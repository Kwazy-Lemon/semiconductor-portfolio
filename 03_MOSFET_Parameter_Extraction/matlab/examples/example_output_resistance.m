clc;
clear;
close all;

%% Add Toolkit

addpath(genpath('..'));

%% Read Dataset

data = read_ltspice_step("../../datasets/raw/Id_Vds.txt");

%% Output Resistance

ro = output_resistance(data);

fprintf("\n");
fprintf("Final Output Resistance = %.4e Ohm\n",ro);
