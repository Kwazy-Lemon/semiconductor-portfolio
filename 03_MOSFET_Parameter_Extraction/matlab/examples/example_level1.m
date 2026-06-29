clc;
clear;
close all;

%% Add Toolkit

addpath(genpath('..'));

%% Read Transfer Characteristics (Id-VGS)

data_transfer = read_ltspice_csv("../../datasets/raw/Id_Vgs.txt");

%% Device Information

data_transfer.VDS = 0.05;
data_transfer.W   = 10e-6;
data_transfer.L   = 1e-6;
data_transfer.Cox = 3.45e-3;

%% Read Output Characteristics (Id-VDS)

data_output = read_ltspice_step("../../datasets/raw/Id_Vds.txt");

%% Level-1 Parameter Extraction

params = level1_extract(data_transfer,data_output);

%% Display Results

fprintf("\n");
fprintf("=========================================\n");
fprintf(" Final Results\n");
fprintf("=========================================\n");
fprintf("Vth    = %.4f V\n",params.Vth);
fprintf("mu     = %.4e m^2/Vs\n",params.mu);
fprintf("lambda = %.4e 1/V\n",params.lambda);
fprintf("ro     = %.4e Ohm\n",params.ro);
fprintf("=========================================\n");
