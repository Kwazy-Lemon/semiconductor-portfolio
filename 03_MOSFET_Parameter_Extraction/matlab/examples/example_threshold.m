clc;
clear;
close all;

%% Add Toolkit Folders

addpath(genpath('..'));

%% Read Dataset

data = read_ltspice_csv('../../datasets/raw/Id_Vgs.txt');

%% Threshold Voltage Extraction

Vth = threshold_voltage(data,"linear");

fprintf("\n");
fprintf("Threshold Voltage = %.4f V\n",Vth);

plot_linear_fit(data,Vth);
