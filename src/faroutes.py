from lima import models
import logging

log = logging.getLogger(__name__)


def includeme(config):
    settings = config.registry.settings.get('lima.fa_settings}}', {})

    # Example to add a specific model
    #config.formalchemy_model("/my_model", package='lima',
    #                         model='lima.models.MyModel')
    #                         **settings)

    log.info('lima.faroutes loaded')
