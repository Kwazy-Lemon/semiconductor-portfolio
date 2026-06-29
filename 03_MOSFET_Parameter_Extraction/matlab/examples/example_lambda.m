clc;
clear;
close all;

addpath(genpath('..'));

data = read_ltspice_step("../../datasets/raw/Id_Vds.txt");

lambda = channel_length_modulation(data);

fprintf("\n");
fprintf("Final Lambda = %.4e 1/V\n",lambda);
