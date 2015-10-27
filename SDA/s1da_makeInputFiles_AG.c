/*
gcc -o s1da_makeInputFiles s1da_makeInputFiles.c -lm
*/

#define MAX_LINE 200

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

main(){
  //char filename[MAX_LINE]="./simplifiedScan1Danalysis_input.dat"
  char *filename;
  FILE *fp;
  char line[MAX_LINE];
  char m2eDefault[MAX_LINE];
  char tmpChar[MAX_LINE];
  unsigned int numRuns,i,j,k;
  int convertMidasFiles;//0.. no (don't convert), 1.. yes
  int plotIndividual;//0.. no (don't convert), 1.. yes
  int plotPositions;//0..no, 1..yes
  unsigned int mcaRange[2];
  unsigned int *runNumbers;
  char scanParameter[MAX_LINE];
  double *scanValues;

  int readValue[2];
  int tmpInt;

  char *datapath;


  filename=malloc(MAX_LINE*sizeof(char));
  filename="./simplifiedScan1Danalysis_input_AG.dat";

  datapath = malloc(MAX_LINE*sizeof(char));
  datapath = "/titan/data1/mpet/PerlRCData/";

  /*read inputfile */
  fp=fopen(filename,"r");
  if(fp==NULL){
    printf("Cannot open input-file:%s\n",filename);
    return(0);
  }

  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"convert Midas files?",19)!=0)){
    printf("unexpected inputfile structure in:'%s'\n",filename);
    return(0);
  }

  convertMidasFiles=0;;
  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"y",1)==0))
    convertMidasFiles=1;


  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"m2e default:",12)!=0)){
    printf("unexpected inputfile structure in:'%s'\n",filename);
    return(0);
  }

  fgets(line,MAX_LINE,fp);
  //char dataDir[30];
  //sscanf(line,"%*s %*s %*s %*s %*s %s",dataDir);
  strncpy(m2eDefault,line,strlen(line)-1);
  m2eDefault[strlen(line)-1]='\0';


  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"MCA Range",8)!=0)){
    printf("unexpected inputfile structure in:'%s'\n",filename);
    return(0);
  }

  fgets(line,MAX_LINE,fp);
  sscanf(line,"%d %d",&mcaRange[0],&mcaRange[1]);

  
  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"Plot Indiviudal?",15)!=0)){
    printf("unexpected inputfile structure in:'%s'\n",filename);
    return(0);
  }

  plotIndividual=0;
  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"y",1)==0))
    plotIndividual=1;
  
  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"Plot Positions?",15)!=0)){
    printf("unexpected inputfile structure in:'%s'\n",filename);
    return(0);
  }
  
  plotPositions=0;
  if((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"y",1)==0))
    plotPositions=1;

  fgets(line,MAX_LINE,fp);
  numRuns=0;
  while((fgets(line,MAX_LINE,fp)!=NULL)&&(strncmp(line,"end",3)!=0)){
    numRuns++;
  }
  fclose(fp);

  runNumbers=malloc(numRuns*sizeof(unsigned int));
  scanValues=malloc(numRuns*sizeof(double));
  
  fp=fopen(filename,"r");
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);
  fgets(line,MAX_LINE,fp);

  for(i=0;i<numRuns;i++){
    fgets(line,MAX_LINE,fp);

    for(j=0;j<strlen(line);j++){
      if(line[j]=='#')
	readValue[0]=j;
      if(line[j]=='>'){
	readValue[1]=j;
	break;
      }
    }

    tmpInt=0;
    for(k=readValue[0]+1;k<readValue[1];k++){
      tmpInt*=10;
      tmpInt+=(line[k]-'0');
    }
    runNumbers[i]=tmpInt;
    // printf("%d ",runNumbers[i]);


    readValue[0]=readValue[1]+2;
    for(k=j;k<strlen(line);k++){
      if(line[k]=='='){
	readValue[1]=k;
	break;
      }
    }

    if(k==strlen(line)){
      printf("error while reading run information\n");
      return(0);
    }


    if(i==0){
      //printf("\n scanParameter: %s\n",scanParameter);
      for(k=readValue[0];k<readValue[1];k++)
	scanParameter[k-readValue[0]]=line[k];
      scanParameter[k-readValue[0]]='\0';
      printf("run number \t%s\n",scanParameter);
    }
    tmpInt=0;
    k=readValue[1]+1;
    while(line[k]!=';'){
      tmpChar[k-readValue[1]-1]=line[k];
      k++;
    }
    tmpChar[k-readValue[1]-1]='\0';
    //printf("%d\t\t%s\t%s\n",runNumbers[i],tmpChar,line);
    scanValues[i]=atof(tmpChar);
    printf("%d\t\t%f\n",runNumbers[i],scanValues[i]);
  }
  fclose(fp);

  /*write inputfiles for matlab and m2e*/
  //m2eseries
  filename="./m2eseries_se.sh";
  fp=fopen(filename,"w");
  if(convertMidasFiles){
    for(i=0;i<numRuns;i++) {
      if(runNumbers[i]<100000) {
        fprintf(fp,"%srun0%d.mid\n",m2eDefault,runNumbers[i]);//attention there is a 0 in the text to account for the runnnumber notation, but as soon as the run number is bigger then 100000 this won't work any more!!!
      } else {
        fprintf(fp,"%srun%d.mid\n",m2eDefault,runNumbers[i]);
      }
    }
  }
  fclose(fp);

  //matlab plotting
  filename="fileListPlotTOF.dat";
  fp=fopen(filename,"w");

  //fprintf(fp,"%d %d\n/home/mpet/sette/simplified1Danalysis/data/\n%d\n%s\n",mcaRange[0],mcaRange[1],plotIndividual,scanParameter);
  //fprintf(fp,"%d %d\n/titan/data1/mpet/PerlRCData/\n%d\n%s\n",mcaRange[0],mcaRange[1],plotIndividual,scanParameter);
  fprintf(fp, "%d %d\n%s\n%d\n%s\n", mcaRange[0], mcaRange[1], datapath, plotIndividual, scanParameter);
  for(i=0;i<numRuns;i++) {
    if(runNumbers[i]<100000) {
      fprintf(fp,"run0%d_se_test.dat %f\n",runNumbers[i],scanValues[i]);//attention there is a 0 in the text to account for the runnnumber notation, but as soon as the run number is bigger then 100000 this won't work any more!!!
    } else {
      fprintf(fp,"run%d_se_test.dat %f\n",runNumbers[i],scanValues[i]);
    }
  }
  fclose(fp);
  
  //matlab position plotting
  filename="fileListPlotPos.dat";
  fp=fopen(filename,"w");
  //fprintf(fp,"%d %d\n/home/mpet/sette/simplified1Danalysis/data/\n%d\n%s\n",mcaRange[0],mcaRange[1],plotPositions,scanParameter);
  fprintf(fp, "%d %d\n%s\n%d\n%s\n", mcaRange[0], mcaRange[1], datapath, plotPositions, scanParameter);
  for(i=0;i<numRuns;i++) {
     if(runNumbers[i]<100000) {
  	fprintf(fp,"%srun0%d_pos.dat %f\n","/triumfcs/trshare/titan/MPET/Data/",runNumbers[i],scanValues[i]);
     } else {
        fprintf(fp,"%srun%d_pos.dat %f\n","/triumfcs/trshare/titan/MPET/Data/",runNumbers[i],scanValues[i]);
     }
  }
  fclose(fp);
}
