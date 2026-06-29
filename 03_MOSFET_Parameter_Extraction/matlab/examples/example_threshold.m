clc;
clear;
close all;

%% Read LTspice Data

data = read_ltspice_csv("Id_Vgs.txt");

%% Threshold Voltage Extraction

Vth = threshold_voltage(data,"linear");

%% Display

disp(Vth)
