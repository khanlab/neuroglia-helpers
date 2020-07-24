#!/usr/bin/env python
import hashlib
import argparse
import re
import os
import subprocess
import errno

#tool to take list of URI's, and create symlinks in SNAKEMAKE_SINGULARITY_DIR



def hash(uri):
        md5hash = hashlib.md5()
        md5hash.update(uri.encode())
        return md5hash.hexdigest()

def get_cached_path(uri):

#parse uri with regular exp to get org, repo, tag:
# group 1 is docker or shub
# group 2 is org (any non-whitespace string)
# group 3 is repo
# group 4 is tag
 
    m = re.search('(?P<hub>\w+)://(?P<org>\S+)/(?P<repo>\S+):(?P<tag>\S+)',uri)
    existing_cache = '{org}_{repo}_{tag}.sif'.format(**m.groupdict())

    singularity_dir = os.environ['SINGULARITY_DIR']
    if m.group('hub') == 'docker':
        pulled_path = os.path.join(singularity_dir,'bids-apps','{org}_{repo}_{tag}.sif'.format(**m.groupdict()))
    elif m.group('hub') == 'shub':
        pulled_path = os.path.join(singularity_dir,'{org}-{repo}-master-{tag}.sif'.format(**m.groupdict()))
    else:
        print('must use docker:// or shub://')

    return pulled_path

def get_linked_path(uri,snakemake_singularity_dir):
    linked_path = os.path.join(snakemake_singularity_dir,hash(uri)+'.simg')
    return linked_path

def make_sym_link(uri,snakemake_singularity_dir):
    cached = get_cached_path(uri)
    linked = get_linked_path(uri,snakemake_singularity_dir )
    if not os.path.exists(cached):
        print(f'ERROR: image {uri} has not already been pulled to {cached}')
    else:
        if os.path.exists(linked):
            print(f'WARNING: link to {cached} already exists in {linked}')
        else:
            subprocess.run(f'ln -s {cached} {linked}',shell=True)
            print(f'linking {cached} in {linked}')

    
#snakemake_singularity_dir = os.environ['SNAKEMAKE_SINGULARITY_DIR']
if 'SNAKEMAKE_SINGULARITY_DIR' in os.environ:
    default_snakemake_singularity_dir = os.environ['SNAKEMAKE_SINGULARITY_DIR']
else:
    default_snakemake_singularity_dir = os.path.join(os.path.expanduser('~'),'.snakemake_singularity')


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--uri', 
                    help='uri of container, {shub/docker}://org/repo:tag')
group.add_argument('--txtfile',#type=argparse.FileType('r'), 
                    help='text file containing uri on each line')
parser.add_argument('--snakemake-singularity-dir',
                    help='Folder to create symlinks to cached singularity images. '
                            'Pass this to snakemake with the --singularity-prefix option,'
                            ' or use a profile that sets this option (e.g. cc-slurm).  '
                            'If set, the SNAKEMAKE_SINGULARITY_DIR environment variable '
                            'will be used for this.  '
                            'Default: {}'.format(default_snakemake_singularity_dir),
                            default=default_snakemake_singularity_dir)

args = parser.parse_args()

#create snakemake_singularity_dir

try:
    os.mkdir(args.snakemake_singularity_dir)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass




if args.uri is not None:
    make_sym_link(args.uri,args.snakemake_singularity_dir)
else:
    #loop through lines of txtfile
    print(args.txtfile)
    with open(args.txtfile) as f:
        for line in f:
            make_sym_link(line.rstrip(), args.snakemake_singularity_dir)

    
   

