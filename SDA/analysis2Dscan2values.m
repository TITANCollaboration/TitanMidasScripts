%%%%%%%%%%%%%%%%%
%%
%% analysisLorentzSteererScan Version 20100715_1100
%%
%%%%%%%%%%%%%%%%%

function analysisLorentzSteererScan

%figure;
data=readData('simplifiedScan1DanalysisPlotting.out');

subplot(1,3,2);
titleString='steerer scan with swapped LS';

dataPoints=size(data,1);


for i=1:dataPoints/2
    dataExtreme1(i,:)=data(2*(i-1)+1,:);    
    dataExtreme2(i,:)=data(2*(i-1)+2,:); 
end




colors={'r','b','k'};
%figure;

subplot(1,3,1)
plotNumIons(dataExtreme1,colors{1});
plotNumIons(dataExtreme2,colors{2});
xlabel('scan value')
ylabel('# ions');
legend('extreme 1','extreme2');


subplot(1,3,2)
plotAvTOF(dataExtreme1,colors{1});
plotAvTOF(dataExtreme2,colors{2});
xlabel('value')
ylabel('<TOF>');
title(titleString,'FontSize',14)

subplot(1,3,3)
plotTOFstd(dataExtreme1,colors{1});
plotTOFstd(dataExtreme2,colors{2});
xlabel('scan value')
ylabel('\sigma_{TOF}');


end


function plotNumIons(data,color);
hold on;
errorbar(data(:,2),data(:,3),data(:,4),color);
hold off;
end

function plotAvTOF(data,color);
hold on;
errorbar(data(:,2),data(:,5),data(:,6),color);
hold off;
end

function plotTOFstd(data,color);
hold on;
plot(data(:,2),data(:,7),color);
hold off;
end


function A= readData(filename)

fid=fopen(filename,'r');
for i=1:1
    tline=fgetl(fid); 
end
d=1;
 while d
     tline=fgetl(fid);   
     if tline==-1;
         break
     end
     
     data(d,:)=sscanf(tline,'%f');    
     
     d=d+1;
 end
 

 fclose(fid);

 A=data;

end
