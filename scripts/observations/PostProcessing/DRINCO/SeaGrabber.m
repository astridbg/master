%Coriolis reader

seaFolder='/home/astridbg/Documents/MC2/ANX_Campaign_copy/DRINCO_Sea';
sFolders=dir(seaFolder);

Tdata=zeros(size(sFolders,1),97);
INPdata=zeros(size(sFolders,1),4);
for i=3:size(sFolders,1)-1
    sampleDir=strcat(seaFolder,'/',sFolders(i).name);
    if contains(sFolders(i).name,'heated')==1
        continue
    end
    load(strcat(sampleDir,'/',sFolders(i).name,'_Frz_T.mat')); %load data
    sampleNum=char(extractBetween(sFolders(i).name,'Sea','_')); % Find sample ID
    sampleName=strcat('Sea',sampleNum); %produce name of sample
    
    sampleTime=char(extractBetween(sFolders(i).name,strcat(sampleName,'_'),'_'));    
    
    INPdata(i,1)=str2double(sampleNum);
    Tdata(i,1)=str2double(sampleNum);   
    
    [FF,FrzT]=Sea2FF(FrzT);
    
    %combine the freezing temperature data for all of the samples
    
    Tdata(i,2:end)=FrzT;
    
end 
    writematrix(transpose(Tdata),'../PostprocessedData/Sea_FrzT.csv')

