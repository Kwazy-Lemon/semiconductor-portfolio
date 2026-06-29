clc;
clear;
close all;

%% Add Toolkit Path

addpath(genpath(".."));

%% Read Dataset

data = read_ltspice_csv("../../datasets/raw/Id_Vgs.txt");

%% Threshold Voltage Extraction

Vth = threshold_voltage(data,"linear");

%% Display Result

fprintf("\n");
fprintf("Threshold Voltage = %.4f V\n",Vth);
