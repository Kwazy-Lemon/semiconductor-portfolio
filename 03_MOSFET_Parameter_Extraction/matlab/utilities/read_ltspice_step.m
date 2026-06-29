function data = read_ltspice_step(filename)
%READ_LTSPICE_STEP Read LTspice .step output file.
%
% Version:
%   v1.0
%
% Author:
%   Jianhao Wu

fid = fopen(filename,'r');

if fid==-1
    error("Cannot open file.");
end

VDS = [];
IDS = [];

start_read = false;

while ~feof(fid)

    line = strtrim(fgetl(fid));

    if isempty(line)
        continue;
    end

    % Skip title
    if startsWith(line,"V2")
        continue;
    end

    % Find first STEP
    if startsWith(line,"Step Information")

        if start_read
            break;
        end

        start_read = true;
        continue;

    end

    if start_read

        nums = sscanf(line,"%f %f");

        if length(nums)==2

            VDS(end+1,1)=nums(1);
            IDS(end+1,1)=nums(2);

        end

    end

end

fclose(fid);

data = struct();

data.Type = "Output";

data.VDS = VDS;

data.IDS = IDS;

fprintf("\n");
fprintf("=====================================\n");
fprintf(" LTspice STEP Import\n");
fprintf("=====================================\n");
fprintf("Samples : %d\n",length(VDS));
fprintf("=====================================\n");

end
