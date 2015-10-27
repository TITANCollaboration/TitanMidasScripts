

function plotTOFspectra
clear;

%plotPositions();

filenameList='fileListPlotTOF.dat';
fid=fopen(filenameList);
d=1;

tline=fgetl(fid);  
mcaRange=sscanf(tline,'%f %f');
tline=fgetl(fid);  
directory=sscanf(tline,'%s');
tline=fgetl(fid); 
plotIndividual=sscanf(tline,'%d');;
tline=fgetl(fid);  
parameter=sscanf(tline,'%s');

legendText=strcat('runNumber and',parameter,'\newline');
while d
    tline=fgetl(fid);   
    if tline==-1;
        break
    end
    filenameData=sscanf(tline,'%s %*s');
    parameterValue(d)=sscanf(tline,'%*s %f');
    fileNr(d)=str2num(filenameData(4:9));
    titleText=strcat(filenameData(1:9),',',parameter,'=',num2str(parameterValue(d)));
    legendText=strcat(legendText,num2str(fileNr(d)),':',num2str(parameterValue(d)),'\newline');
    [numIons(d) meanTOF(d) stdev(d)]=readProcessPrintData(directory,filenameData,d,mcaRange,titleText,plotIndividual);
    d=d+1;
end
fclose(fid);




% %numIons(1:25)=numIons(1:25)/4;

figure('Name','Simplified Scan1D Analysis: Final Plots');
%screenAPrintSize(1)
subplot(1,4,1);
errorbar(parameterValue,numIons,sqrt(numIons),'.-');
xlabel(parameter);
ylabel('# ions');
yRange=ylim;

%line([1936 1936],yRange,'Color','r');

subplot(1,4,2);
errorbar(parameterValue,meanTOF,stdev./sqrt(numIons),'.-');
xlabel(parameter);
ylabel('<TOF> [\mus]');

subplot(1,4,3);
plot(parameterValue,stdev,'.-','MarkerSize',15);
xlabel(parameter);
ylabel('std TOF [\mus]');
scrsz = get(0,'ScreenSize');
set(gcf,'Position',[10 10 scrsz(3)-50 scrsz(4)/2-150 ])
yRange=ylim;
xRange=xlim;
text(xRange(1)+1*(xRange(2)-xRange(1)),yRange(1)+0.5*(yRange(2)-yRange(1)),legendText,'FontSize',10);

 
fid=fopen('simplifiedScan1DanalysisPlotting.out','w');
fprintf(fid,'# srun#\t%s\t#ions\terr\t\t<TOF>\t\terr\t\tstd TOF\n',parameter);
for i=1:size(parameterValue,2)
    fprintf(fid,'%d\t%f\t%d\t%f\t%f\t%f\t%f\n',fileNr(i),parameterValue(i),numIons(i),sqrt(numIons(i)),meanTOF(i),stdev(i)/sqrt(numIons(i)),stdev(i));
end

fclose(fid);
% format long;
% 'parameterValue numIons meanTOF stdev'
% [parameterValue' numIons' meanTOF' stdev'] 

%plotPositions()
end

function [numIons meanTOF err]=readProcessPrintData(directory,filenameData,subplotNr,mcaRange,titleText,plotIndividual)

if(plotIndividual&&(mod(subplotNr-1,4)==0))
    figure('Name',strcat('Simplified Scan1D Analysis: Individual Runs (first file:',filenameData,')'));
    screenAPrintSize(1)
end

if(plotIndividual)
  subplot(3,4,subplotNr-4*max([0,floor((subplotNr-1)/4)]));
end

fid=fopen(strcat(directory,filenameData));
if(fid==1)
    tmpText=strcat('cannot open file:',filenameData);
    disp(tmpText);
    if(plotIndividual)
        yRange=ylim;
        xRange=xlim;
        text(xRange(1)+0.1*(xRange(2)-xRange(1)),yRange(1)+0.6*(yRange(2)-yRange(1)),tmpText,'FontSize',10,'Interpreter','none');
    end
    numIons=0;
    meanTOF=0;
    err=0;
    return
end


fgetl(fid);
d=1;
while d
    tline=fgetl(fid);   
    if tline==-1;
        break
    end
    data(d,:)=sscanf(tline,'%d %d %d');
    d=d+1;
end

if d==1
    tmpText=strcat('no data in file:',filenameData);
    disp(tmpText);
    numIons=0;
    meanTOF=0;
    err=0;
    return
end

fclose(fid);
sortedData(1:5000)=0;

for i=1:size(data,1)
    if (data(i,2)>0)  %CHECK IF THIS IS RIGHT!!!! If did not used to be here!!!!
    
        sortedData(data(i,2))=sortedData(data(i,2))+data(i,3);
    end
end


x=0.2:0.2:500;

mcaRangeInt=floor(mcaRange/0.2-1);
mcaRangeInt(1)=mcaRangeInt(1)+1;
mcaRangeInt(2)=mcaRangeInt(2)+1;

mcaRange=mcaRangeInt*0.2+0.2;
numIons=sum(sortedData(mcaRangeInt(1):mcaRangeInt(2)));  
[meanTOF err]=calcMeanTOF(x(mcaRangeInt(1):mcaRangeInt(2)),sortedData(mcaRangeInt(1):mcaRangeInt(2)));


if(plotIndividual)
    plot(x,sortedData);
    xlabel('MCA: time of flight [\mus]');
    ylabel('# of counts');
    title(titleText);
    yRange=ylim;
    xRange=xlim;
    line([mcaRange(1),mcaRange(1)],yRange,'Color','r')
    line([mcaRange(2),mcaRange(2)],yRange,'Color','r')
    tmpText=strcat('region of interest \newline (mcaRange:',num2str(mcaRange(1)),'-',num2str(mcaRange(2)),') \newline');
    tmpText=strcat(tmpText,'# of ions=',num2str(numIons),'\newline');
    tmpText=strcat(tmpText,'<TOF>=',num2str(meanTOF),'\newline');
    tmpText=strcat(tmpText,'\sigma=',num2str(err));
    text(xRange(1)+0.5*(xRange(2)-xRange(1)),yRange(1)+0.6*(yRange(2)-yRange(1)),tmpText,'FontSize',10);

    scanValues=41;
    resonance(1:scanValues)=0;
    resonanceCounts(1:scanValues)=0;
    for i=1:size(data,1)
        if((data(i,2)<=mcaRangeInt(2))&& (data(i,2)>=mcaRangeInt(1)))
            k=mod(data(i,1),scanValues)+1;
            resonance(k)=resonance(k)+x(data(i,2))*data(i,3);
            resonanceCounts(k)=resonanceCounts(k)+data(i,3);
        end
    end
    resonance=resonance./resonanceCounts;

    resonanceError(1:scanValues)=0;
    for i=1:size(data,1)
        if((data(i,2)<=mcaRangeInt(2))&& (data(i,2)>=mcaRangeInt(1)))
            k=mod(data(i,1),scanValues)+1;
            resonanceError(k)=resonanceError(k)+(x(data(i,2))-resonance(k))^2*data(i,3);
        end
    end

%uncertainty on resonance: NOT A VERY GOOD WAY OF DOING IT!!
    for i=1:scanValues
        if(resonanceCounts==1)
            resonanceError(i)=err;
        else
            resonanceError(i)=sqrt(resonanceError(i)/(resonanceCounts(i)-1)/resonanceCounts(i));
        end
    end


    subplot(3,4,subplotNr+4-4*max([0,floor((subplotNr-1)/4)]));
    scanValues=1:scanValues;
    plot(scanValues,resonance,'k');
    hold on;
    errorbar(scanValues,resonance,resonanceError,'.r');
    hold off;
    xlabel('scan value #');
    ylabel('<TOF> [\mus]');
    title(filenameData(1:9));
    xlim([1 max(scanValues)]);
    %ylim([20 34]);
    
    subplot(3,4,subplotNr+8-4*max([0,floor((subplotNr-1)/4)]));
    plot(scanValues,resonanceCounts,'k');
    hold on;
    errorbar(scanValues,resonanceCounts,resonanceCounts.^(1/2),'.r');
    hold off;
    xlabel('scan value #');
    ylabel('#ions');
    title(filenameData(1:9));
    xlim([1 max(scanValues)]);
    %ylim([20 34]);
    
    
    
    
end

end


function [A B]=calcMeanTOF(x,data)
mean=0;
std1=0;
n=max(size(data));
for i=1:n
    mean=mean+x(i)*data(i);
end
A=mean/sum(data);

for i=1:n
    std1=std1+((x(i)-A)^2)*(data(i));
end
B=sqrt(std1/(sum(data)-1));

end

%subfunction to set screen size and printing size of figure
function screenAPrintSize(landscape)
    %%landscape=0;
    scrsz = get(0,'ScreenSize');
    set(gcf,'Position',[10 50 scrsz(3)/1-50 scrsz(4)/1-150 ])
    
    set(gcf,'PaperType','usletter');
    if landscape==1
        set(gcf,'PaperOrientation','landscape');
    else
        set(gcf,'PaperOrientation','portrait');
    end
    set(gcf,'PaperPosition', [0.25 0.25 get(gcf,'PaperSize')-0.5]);
end


function plotPositions
	filenameList='fileListPlotPos.dat';
	fid=fopen(filenameList);
	d=1;
	
	tline=fgetl(fid);  
	mcaRange=sscanf(tline,'%f %f');
	tline=fgetl(fid);  
	directory=sscanf(tline,'%s');
	tline=fgetl(fid); 
	plotPosition=sscanf(tline,'%d');;
	tline=fgetl(fid);  
	parameter=sscanf(tline,'%s');
	
	legendText=strcat('runNumber and',parameter,'\newline');
	
	if plotPosition==0;
		return
	end
	
	numSubPlot=9;
	figure;
	while d
	    tline=fgetl(fid);   
	    if tline==-1;
	        break
	    end
	    filenameData=sscanf(tline,'%s %*s');
	    parameterValue(d)=sscanf(tline,'%*s %f');
	    ppValue=sscanf(tline,'%*s %s');
	    fin=fopen(filenameData);
	    dd=1;
	    x = [];
	    y = [];
	    if fid~=-1;
		    while dd
		    	tline=fgetl(fin);
			if tline==-1;
		      	     break
		   	end
			x(dd)=sscanf(tline,'%d %*d');
			y(dd)=sscanf(tline,'%*d %d');
			dd=dd+1;
	  	    end
		    fclose(fin);
	    else
	    	tmpText=strcat('Cannot open file: ',filenameData);
		disp(tmpText);
	    end
	    hack=0;
	    if mod(d,numSubPlot)==0;
	    	hack=numSubPlot;
	    end
	    subplot(3,3,mod(d,numSubPlot)+hack);
	    plot(x,y,'.');
	    axis([0 256 0 256]);
	    axis square;
	    xlabel(ppValue);
	    
	    %fileNr(d)=str2num(filenameData);
	    %titleText=strcat(filenameData(1:9),',',parameter,'=',num2str(parameterValue(d)));
	    %legendText=strcat(legendText,num2str(fileNr(d)),':',num2str(parameterValue(d)),'\newline');
	    %[numIons(d) meanTOF(d) stdev(d)]=readProcessPrintData(directory,filenameData,d,mcaRange,titleText,plotIndividual);
	    %d=d+1;
	    if mod(d,numSubPlot)==0;
	    	figure;
	    end
	    d=d+1;
	end
	fclose(fid);	
end

