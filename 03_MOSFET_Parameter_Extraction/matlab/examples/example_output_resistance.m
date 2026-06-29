clc;
clear;
close all;

addpath(genpath('..'));

data = read_ltspice_step("../../datasets/raw/Id_Vds.txt");

ro = output_resistance(data);

fprintf("\n");
fprintf("Final Output Resistance = %.4e Ohm\n",ro);
