import io
import json
import logging
import shutil
import tempfile

import six
import yaml
from vcr_unittest import VCRTestCase

from c7n import policy
from c7n.schema import generate, validate as schema_validate
from c7n.ctx import ExecutionContext
from c7n.utils import CONN_CACHE
from c7n.resources import load_resources
from c7n_azure.session import Session

load_resources()
C7N_SCHEMA = generate()


class BaseTest(VCRTestCase):

    def _get_vcr_kwargs(self):
        return super(BaseTest, self)._get_vcr_kwargs(
            filter_headers=[('Authorization', 'bearer filtered')],
        )

    def cleanUp(self):
        # Clear out thread local session cache
        CONN_CACHE.session = None

    def get_temp_dir(self):
        """ Return a temporary directory that will get cleaned up. """
        temp_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, temp_dir)
        return temp_dir

    def get_context(self, config=None, policy=None):
        if config is None:
            self.context_output_dir = self.get_temp_dir()
            config = Config.empty(output_dir=self.context_output_dir)
        ctx = ExecutionContext(
            Session,
            policy or Bag({'name': 'test-policy'}),
            config)
        return ctx

    def load_policy(
            self, data, config=None):
        errors = schema_validate({'policies': [data]}, C7N_SCHEMA)
        if errors:
            raise errors[0]

        config = config or {}

        temp_dir = self.get_temp_dir()
        config['output_dir'] = temp_dir

        conf = Config.empty(**config)
        p = policy.Policy(data, conf, Session)
        p.validate()
        return p

    def capture_logging(
            self, name=None, level=logging.INFO,
            formatter=None, log_file=None):
        if log_file is None:
            log_file = TextTestIO()
        log_handler = logging.StreamHandler(log_file)
        if formatter:
            log_handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.addHandler(log_handler)
        old_logger_level = logger.level
        logger.setLevel(level)

        @self.addCleanup
        def reset_logging():
            logger.removeHandler(log_handler)
            logger.setLevel(old_logger_level)

        return log_file


class Bag(dict):

    def __getattr__(self, k):
        try:
            return self[k]
        except KeyError:
            raise AttributeError(k)


class Config(Bag):

    @classmethod
    def empty(cls, **kw):
        d = {}
        d.update({
            'region': None,
            'regions': None,
            'cache': '',
            'profile': None,
            'account_id': None,
            'assume_role': None,
            'external_id': None,
            'log_group': None,
            'metrics_enabled': False,
            'output_dir': '',
            'cache_period': 0,
            'dryrun': False})
        d.update(kw)
        return cls(d)


class TextTestIO(io.StringIO):

    def write(self, b):

        # print handles both str/bytes and unicode/str, but io.{String,Bytes}IO
        # requires us to choose. We don't have control over all of the places
        # we want to print from (think: traceback.print_exc) so we can't
        # standardize the arg type up at the call sites. Hack it here.

        if not isinstance(b, six.text_type):
            b = b.decode('utf8')
        return super(TextTestIO, self).write(b)