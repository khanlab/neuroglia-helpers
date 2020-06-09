#!/usr/bin/env python3

# Aim: validate bids-apps.tsv
#    each row: have 4 columns
#    2nd column(url):must star with "docker://" or "shub://", for instance 
#        gradcorrect_v0.0.2', 'docker://khanlab/gradcorrect:v0.0.2
#    1st column(name): match 2nd columns' docker image name and tag part
#    2nd column(url): docker/shub image exist on the hub.
#    3rd column(base_option): '' or start with '-'
#    4th column(job_template): a string match a job name in folder job-templates
#
# Note:
#    use '#' to ignore the validation a line in bids-apps.tsv

import csv
import os

# set validate_image to Ture, will validate docker image(docker pull) and singularity image(singularity pull), may take a very long time...
validate_image = False

#########
# get job_template list 
#########

#get files under folder job-templates
job_templates_files = os.listdir("job-templates")
#remove file name ext: .job
job_templates = [e[:-4] for e in job_templates_files]

#########
# validate bids-apps.tsv
#########

line_index = 0
with open("bids-apps.tsv") as fd:
    rd = csv.reader(fd, delimiter="\t", quotechar='"')
    for row in rd:

        # line# start with 1
        line_index = line_index+1

        #each row must has 4 columns
        if len(row) != 4:
            raise ValueError("LINE {} ERROR: each row must has 4 columns".format(line_index))

        #parse
        name=row[0]
        url=row[1]
        base_options=row[2]
        job_template=row[3]

        # skip 1st row
        if name=="name":
            continue
        
        # skip comment
        if name[0]=="#":
            continue
        
        #########
        #url must star with "docker://" or "shub://"
        #########

        if url.startswith("docker://") or url.startswith("shub://") or url.startswith("file://"):
            pass
        else:
            raise ValueError("LINE {} ERROR: url must star with 'docker://' or 'shub://'  or 'file://' ".format(line_index))    
        
        #########
        #docker_image_name_and_tag == name
        #    docker://khanlab/gradcorrect:v0.0.2 docker_image_name_and_tag： gradcorrect:v0.0.2
        #    name: gradcorrect_v0.0.2 
        
        # or 

        #docker_image_name_and_tag in name 
        #    docker://khanlab/prepdwi:v0.0.12
        #    prepdwi_v0.0.12d_bedpost
        #########

        # docker_image_name_and_tag = url.split('/')[-1]
        # replaced = docker_image_name_and_tag.replace(":","_")
        # if  replaced not in name:
        #     raise ValueError("LINE {} ERROR: name NOT match with docker image's name and tag".format(line_index))    
        
        #########
        # check if docker/singularity image exist
        #########
        if url.startswith("docker://"):
            # remove images after pull to avoid "no space left on device"
            cmd = "docker pull {} > /dev/null && docker rmi -f $(docker images -q)".format(url[9:])
            print(cmd)
            if validate_image:
                os.system(cmd)

        if url.startswith("shub://"):
            cmd = "singularity pull {} --name temp.img  > /dev/null && rm temp.img".format(url[7:])
            print(cmd)
            if validate_image:
                os.system(cmd)

        #########
        # base_options must be '' or start with '-'
        #########
        if base_options =="" or base_options.startswith(""):
            pass
        else:
            raise ValueError("LINE {} ERROR: base_options must be '' or start with '-' ".format(line_index))    
       
        #########
        #job_template must be a string match a job name in folder job-templates
        #########
        if job_template not in job_templates:
            raise ValueError("LINE {} ERROR: job_template must match with one job in job-templates".format(line_index))    

        