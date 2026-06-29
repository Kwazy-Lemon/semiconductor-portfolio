clc;
clear;
close all;

addpath(genpath('..'));

data = read_ltspice_step("../../datasets/raw/Id_Vds.txt");
