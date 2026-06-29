clc;
clear;
close all;

%% Add Toolkit Folders

addpath(genpath('..'));

%% Read Dataset

data = read_ltspice_csv("../../datasets/raw/Id_Vgs.txt");

%% Device Information

data.VDS = 0.05;

data.W = 10e-6;

data.L = 1e-6;

data.Cox = 3.45e-3;

%% Threshold Voltage Extraction

Vth = threshold_voltage(data,"linear");

fprintf("\n");
fprintf("Threshold Voltage = %.4f V\n",Vth);

plot_linear_fit(data,Vth);
