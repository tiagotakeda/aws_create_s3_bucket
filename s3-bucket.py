#!/usr/bin/python

import os, sys
import subprocess
from subprocess import *

def entradas():
    name = str(input("\nBucket name: ")) 

    print("\nChoose one of the regions listed below: ")
    print("\n1) US East (N. Virginia)")
    print("2) US East (Ohio)")
    print("3) US West (N. California)")
    print("4) US West (Oregon)")
    print("5) Africa (Cape Town)")
    print("6) Asia Pacific (Hong Kong)")
    print("7) Asia Pacific (Mumbai)")
    print("8) Asia Pacific (Osaka)")
    print("9) Asia Pacific (Seoul)")
    print("10) Asia Pacific (Singapore)")
    print("11) Asia Pacific (Sydney)")
    print("12) Asia Pacific (Tokyo)")
    print("13) Canada (Central)")
    print("14) Europe (Frankfurt)")
    print("15) Europe (Ireland)")
    print("16) Europe (London)")
    print("17) Europe (Milan)")
    print("18) Europe (Paris)")
    print("19) Europe (Stockholm)")
    print("20) Middle East (Bahrain)")
    print("21) South America (São Paulo)")

    while True:
        r = int(input("\nRegion: "))
        
        if r == 1:
            region = "us-east-1"
            break
        elif r == 2:
            region = "us-east-2"
            break
        elif r == 3:
            region = "us-west-1"
            break
        elif r == 4:
            region = "us-west-2"
            break
        elif r == 5:
            region = "af-south-1"
            break
        elif r == 6:
            region = "ap-east-1"
            break
        elif r == 7:
            region = "ap-south-1"
            break
        elif r == 8:
            region = "ap-northeast-3"
            break
        elif r == 9:
            region = "ap-northeast-2"
            break
        elif r == 10:
            region = "ap-southeast-1"
            break
        elif r == 11:
            region = "ap-southeast-2"
            break
        elif r == 12:
            region = "ap-northeast-1"
            break
        elif r == 13:
            region = "ca-central-1"
            break
        elif r == 14:
            region = "eu-central-1"
            break
        elif r == 15:
            region = "eu-west-1"
            break
        elif r == 16:
            region = "eu-west-2"
            break
        elif r == 17:
            region = "eu-south-1"
            break
        elif r == 18:
            region = "eu-west-3"
            break
        elif r == 19:
            region = "eu-north-1"
            break
        elif r == 20:
            region = "me-south-1"
            break
        elif r == 21:
            region = "sa-east-1"
            break
        else:
            print("\n\t\tInvalid region. Try again")

    access_key_id = str(input("ACCESS KEY ID: "))
    secret_access_key = str(input("SECRET ACCESS KEY: "))

    return name, region, access_key_id, secret_access_key

def escrita(name, region):
    parent_dir = os.getcwd()
    path = os.path.join(parent_dir, name)

    os.mkdir(path)
    print("\nDirectory '% s' created" % name)
    
    os.chdir(path)
    
    variables = os.open("variables.tf", os.O_RDWR|os.O_CREAT)
    
    s_variables = ["variable \"region\" {\n", "\tdescription = \"Value that descibes the aws region\"\n", 
        "\ttype        = string\n", "\tdefault     = \"", region, "\"\n", "}\n", "\n", 
        "variable \"bucket_name\" {\n", "\tdescription = \"Value that sets the bucket name\"\n", 
        "\ttype        = string\n", "\tdefault     = \"", name, "\"\n", "}"]
    
    for i in s_variables:
        line = str.encode(i)
        num = os.write(variables, line)

    os.close(variables)


    main = os.open("main.tf", os.O_RDWR|os.O_CREAT)
    
    s_main = ["terraform {\n", "\trequired_providers {\n", "\t\taws = {\n", 
        "\t\t\tsource  = \"hashicorp/aws\"\n", "\t\t\tversion = \"~> 3.27\"\n", "\t\t}\n", "\t}\n",
        "\n", "\trequired_version = \">= 0.14.9\"\n", "}\n", "\n", "provider \"aws\" {\n", 
        "\tprofile = \"default\"\n", "\tregion  = var.region\n", "}\n", "\n"
        "resource \"aws_s3_bucket\" \"b\" {\n", "\tbucket = var.bucket_name\n", 
        "\tacl\t= \"private\"\n", "\n", "\ttags = {\n", "\t\tEnviroment = \"Dev\"\n", "\t}\n", "}"]
    
    for i in s_main:
        line = str.encode(i)
        num = os.write(main, line)

    os.close(main)

def main():
    print("\t\t\tDESAFIO TÉCNICO DAREDE")

    name, region, access_key_id, secret_access_key = entradas()

    escrita(name, region)

    configure_access_key = "aws configure set aws_access_key_id " + access_key_id
    configure_secret_key = "aws configure set aws_secret_access_key " + secret_access_key

    p1 = subprocess.run('terraform init', shell=True)

    p2 = subprocess.Popen(configure_access_key, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p2_out = p2.communicate(configure_access_key)
    p3 = subprocess.Popen(configure_secret_key, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    p3_out = p2.communicate(configure_secret_key)

    p3 = subprocess.run('terraform apply -auto-approve', shell=True)   

main()