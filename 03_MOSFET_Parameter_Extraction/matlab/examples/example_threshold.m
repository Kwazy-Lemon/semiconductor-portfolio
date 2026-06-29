clc;
clear;
close all;

addpath(genpath('..'));

data = read_ltspice_csv("../../datasets/raw/Id_Vgs.txt");

data.VDS = 0.05;

data.W = 10e-6;

data.L = 1e-6;

data.Cox = 3.45e-3;

Vth = threshold_voltage(data,"linear");

mu = mobility(data);

fprintf("\n");
fprintf("Threshold Voltage = %.4f V\n",Vth);

plot_linear_fit(data,Vth);
