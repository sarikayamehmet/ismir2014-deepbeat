'''
Created on May 4, 2014

@author: sstober
'''

import os;
import sys;

import logging;
log = logging.getLogger(__name__);

# from pylearn2.utils.timing import log_timing

from deepbeat.util import load_config;
from deepbeat.pylearn2ext.util import merge_params;

from deepbeat.eeg.run.train_convnet import train_convnet;
from deepbeat.eeg.run.train_sda_mlp import train_mlp;

from config import Config;

def process_jobs(config):
    common_config = config.common;
    for job in config.jobs:
        log.info('Processing job {} with base {}'.format(job.name, job.base));
        job_config = merge_params(common_config, config[job.base]);
        log.debug('job overrides: {}'.format(job.overrides));
        job_config = merge_params(job_config, job.overrides);
        
        job_config.experiment_root = os.path.join(
                                                  config.output_root,
                                                  job_config.type,
                                                  job.name
                                                  );
        log.debug('experiment root: {}'.format(job_config.experiment_root));
        
        print job_config;
        
#         try:
        if job_config.type == 'cnn':
            train_convnet(job_config);                
        elif job_config.type == 'fftcnn':
            train_convnet(job_config);
        elif job_config.type == 'sda':
            train_mlp(job_config);
        else:
            log.error('unsupported job type {}'.format(job_config.type));
 
#         except:
#             log.fatal("Unexpected error:", sys.exc_info());

if __name__ == '__main__':
    default_config = os.path.join(os.path.dirname(__file__), 'batch.cfg');    
    config = load_config(default_config=default_config, reset_logging=False);
                         
    config = merge_params(Config(file(default_config)), config);
                         
    process_jobs(config);
