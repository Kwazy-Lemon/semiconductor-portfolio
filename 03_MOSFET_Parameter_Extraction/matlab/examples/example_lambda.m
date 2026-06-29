clc;
clear;
close all;

%% Add Toolkit Folders

addpath(genpath('..'));

%% Read Dataset

data = read_ltspice_csv("../../datasets/raw/Id_Vds.txt");

%% Device Information

data.VGS = 5;          % Gate bias during output characteristics

%% Channel-Length Modulation

lambda = channel_length_modulation(data);

fprintf("\n");
fprintf("=====================================\n");
fprintf("Lambda = %.4e 1/V\n",lambda);
fprintf("=====================================\n");
