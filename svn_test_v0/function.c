#include "stdio.h"
#include "stdlib.h"
#include "conio.h"
#include "windows.h"
#include "io.h"
#include "dir.h"
#include "string.h"
#include "function.h"
#include "md5.h"

int isCreate = 0;

char *GetSvnPath(void) //获取svn文件夹的路径
{
    char *buf =(char*)calloc(100,sizeof(char*));
    GetModuleFileName(NULL,buf,MAX_PATH);
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\svn");
    return buf;
}

int Create(void)  //创建svn文件夹
{
    int i=1;
    char *buf=GetSvnPath();
    i= mkdir(buf);
    if(i == 0)
    {
        printf("创建成功\n");
    }
    else if(!access(buf,0))
    {
        printf("项目已经存在\n");
    }
    else
    {
        printf("创建失败\n");
    }
    if (IsFile_svn("version0")==0)
    {
        buf=GetSvnPath();
        strrchr( buf, '\\')[0]= 0;
        strcat(buf,"\\version0");
        mkdir(buf);
    }
    if (IsFile_svn("version.txt")==0)
    {
        buf=GetSvnPath();
        strcat(buf,"\\version.txt");
        FILE *fp;
        fp=fopen(buf,"a+");
        fprintf(fp,"0 root 0\n");
        fclose(fp);
    }
    if (IsFile_svn("version_hold.txt")==0)
    {
        buf=GetSvnPath();
        strcat(buf,"\\version_hold.txt");
        FILE *fp;
        fp=fopen(buf,"w+");
        fprintf(fp,"1 0");
        fclose(fp);
    }
    return 0;
}

int Status(void)    //维护并打印状态表（status.txt）
{
    struct _finddata_t files;
    int File_Handle;            //File_Handle是文件对应句柄
    int i=0;                  //i是文件数
    char buf[80];
    char* svn_path=GetSvnPath();  //svn_path是svn文件夹下txt（状态表）的路径
    strcat(svn_path,"\\status.txt");

    char FileStatus[30];            //用来读出和修改文件状态
    FILE *sta_txt;
    GetModuleFileName(NULL,buf,MAX_PATH);
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\*.*");
    //修改statu.txt中未受管理项的标志位
    File_Handle = _findfirst(buf,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0 && files.attrib != _A_SUBDIR)
        {
            if(i==0)
            {
                sta_txt=fopen(svn_path,"a+");
            }
            if(IsConFile(files.name)==0 && IsInStatus(files.name)==0)
            {
                fseek(sta_txt,0,SEEK_END);
                //printf("%s\n",files.name);
                fprintf(sta_txt,"? %s\n",files.name);
            }
            i++;
        }
    }while(0==_findnext(File_Handle,&files));
    fclose(sta_txt);

    //修改status.txt中那些改变了的文件的标志位

    File_Handle = _findfirst(buf,&files);
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0 && files.attrib != _A_SUBDIR)
        {
            if (IsConFile(files.name)==1)
            {
               if(Compare(files.name)==0)
               {
                   ChangeStatus(files.name,'M');
               }

            }
        }
    }while(0==_findnext(File_Handle,&files));

    //修改status中丢失文件的标志位
   Txtname();
    char* name_txt_path=GetSvnPath();  //name_txt_path是svn文件夹下name.txt（名字表）的路径
    strcat(name_txt_path,"\\name.txt");
    FILE *fp;
    char* ConTxt_path=GetSvnPath();  //ConTxt_path是svn文件夹下control_name.txt（受管理表）的路径
    strcat(ConTxt_path,"\\control_name.txt");
    FILE *ConTxt;
    char name[50]={0};
    char copyname[50]={0};
    char name1[50]={0};
    char copyname1[50]={0};
    int IfExit=0;
    if(ConTxt=fopen(ConTxt_path,"r"))
    {
         while(fgets(name,50,ConTxt) != NULL)
        {
            memset(copyname,'\0',sizeof(copyname));
            strncpy(copyname,name,strlen(name)-1);
            strrchr(copyname,' ')[0]= 0;
            if(fp=fopen(name_txt_path,"r"))
            {
                while(fgets(name1,50,fp) != NULL && IfExit==0)
                {
                    memset(copyname1,'\0',sizeof(copyname1));
                    strncpy(copyname1,name1,strlen(name1)-1);
                    if(strcmp(copyname,copyname1)==0)
                    {
                        IfExit=1;
                    }
                }
                fclose(fp);
            }
            if(IfExit==0)
            {
                fclose(ConTxt);
                char command[50]="delete ";
                strcat(command,copyname);
                DelConFile(command);
                ChangeStatus(copyname,'G');
                ConTxt=fopen(ConTxt_path,"r");
            }
            IfExit=0;
        }
    }
    fclose(ConTxt);
    //****************修改未受管理的删除项************************
   Txtname();
    FILE *newstatxt;
    char *copy_path=GetSvnPath();
    strcat(copy_path,"\\tmp.txt");
    sta_txt=fopen(svn_path,"r+");
    newstatxt=fopen(copy_path,"w");
    while(fgets(name,50,sta_txt))
    {
        memset(copyname,'\0',sizeof(copyname));
        strncpy(copyname,name+2,strlen(name)-3);
        if(IsFile(copyname)==1 || name[0]=='G')
        {
            fprintf(newstatxt,"%s",name);
        }
    }
    fclose(sta_txt);
    fclose(newstatxt);
    remove(svn_path);//删除原文件
    rename(copy_path,svn_path);//将临时文件名改为原文件名

    //×××××××××××××××输出status表××××××××××××××××××××
    if(sta_txt=fopen(svn_path,"r"))
    {
        while(fgets(FileStatus,30,sta_txt))
        {
            if(FileStatus[0] != 'N')
            {
                printf("%s",FileStatus);
            }
        }
    }
    fclose(sta_txt);
    _findclose(File_Handle);
    return 0;
}

void ChangeStatus(char *filename,char c)//修改status的标志位‘c’
{
    char* svn_path=GetSvnPath();  //svn_path是svn文件夹下txt（状态表）的路径
    strcat(svn_path,"\\status.txt");
    FILE *sta_txt;
    sta_txt=fopen(svn_path,"r+");
    int Ifexit=0;
    char buffer[64]={0};
    char copybuffer[64]={0};
    while(fgets(buffer, 64, sta_txt) != NULL)
    {
        memset(copybuffer,'\0',sizeof(copybuffer));
        strncpy(copybuffer,buffer,strlen(buffer)-1);
        strcpy(copybuffer,copybuffer+2);
        if(strcmp(copybuffer,filename)==0)
        {
            Ifexit=1;
            buffer[0]=c;
            fseek(sta_txt,-strlen(buffer)-1,SEEK_CUR);
            fprintf(sta_txt,"%s",buffer);
            fclose(sta_txt);
        }
    }
    //************有种特殊情况，即一次都没有status时就add*************************
    if(Ifexit==0)
    {
        sta_txt=fopen(svn_path,"a+");
        char tmp[4]="+ ";
        strcat(tmp,filename);
        fprintf(sta_txt,"%s\n",tmp);
        fclose(sta_txt);
    }
}

int Getcommand(char *command)    //获取输入命令
{
    int if_exit=0;          //判断是否退出
    int choice=-2;
    if (strcmp(command,"create")==0 )
    {
        isCreate = 1;
        choice=0;
    }
    else if(strcmp(command,"status")==0)
    {
        choice=1;
    }
    else if(strncmp(command,"add",3)==0)
    {
        choice=2;
    }
    else if(strncmp(command,"delete",6)==0)
    {
        choice=3;
    }
    else if(strncmp(command,"commit",6)==0)
    {
        choice=4;
    }
    else if(strncmp(command,"update",6)==0)
    {
        choice=5;
    }
    else if(strcmp(command,"revert")==0)
    {
        choice=6;
    }
    else if(strncmp(command,"log",3)==0)
    {
        choice=7;
    }
    else if(strncmp(command,"attribute",9)==0)
    {
        choice=8;
    }
    else if(strcmp(command,"quit")==0)
    {
        choice=-1;
    }

    switch(choice)
    {
        case 0:
                Create();
                break;
        case 1:
              if (isCreate == 0)break;
                Status();
                break;
        case 2:
               if (isCreate == 0)break;
                Addfile(command);
                break;
        case 3:
               if (isCreate == 0)break;
                DelFile(command);
                break;
        case 4:
               if (isCreate == 0)break;
                Commit(command);
                break;
        case 5:
               if (isCreate == 0)break;
                Update(command,0);
                break;
        case 6:
               if (isCreate == 0)break;
                Revert();
                break;
        case 7:
             if (isCreate == 0)break;
                log(command);
                break;
        case 8:
               if (isCreate == 0)break;
                Attribute(command);
                break;
        case -1:
                if_exit=-1;
                break;
        default:
                printf("Wrong command!\n");
                break;
    }
    if (if_exit == -1)
    {
        return -1;
    }
    return 0;
}

int Addfile(char *command)      //添加受管理文件到contorl文本，并修改status文本
{
    char f_name[50]={0};        //文件名字
    char buffer[64]={0};
    char* svn_path=GetSvnPath();  //svn_path是svn文件夹下txt（状态表）的路径
    strcat(svn_path,"\\status.txt");
    char* ConTxt_path=GetSvnPath();  //ConTxt_path是svn文件夹下control_name.txt（受管理表）的路径
    strcat(ConTxt_path,"\\control_name.txt");
    if(strlen(command)<5)
    {
        printf("wrong input!");
        return 0;
    }
    strncpy(f_name,command+4,strlen(command)-4);

    if(IsConFile(f_name)==1)
    {
        printf("this file has been a controled file\n");
        return 0;
    }

    if(IsFile(f_name)==0)
    {
        printf("This is not a file name.\n");
        return 0;
    }
    //修改status.txt的内容
    ChangeStatus(f_name,'+');

    //将文件加入受管理列表
    char* file_path=GetSvnPath();  //file_path是add文件的路径
    strrchr(file_path, '\\')[0]= 0;
    strcat(file_path,"\\");
    strcat(file_path,f_name);
    FILE *ConTxt;
    char *md5;
    md5=MD5_file(file_path,32);
    ConTxt=fopen(ConTxt_path,"a+");
    fprintf(ConTxt,"%s %s\n",f_name,md5);
    fclose(ConTxt);
}

int Txtname()    //name.txt用于保存当前工作区所有的文件名，每次调用会重写
{
    char* name_txt_path=GetSvnPath();  //name_txt_path是svn文件夹下name.txt（名字表）的路径
    strcat(name_txt_path,"\\name.txt");
    FILE *fp;
    struct _finddata_t files;
    char buf[80];
    int i=0;
    int File_Handle;            //File_Handle是文件对应句柄
    GetModuleFileName(NULL,buf,MAX_PATH);
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\*.*");
    File_Handle = _findfirst(buf,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0 && files.attrib != _A_SUBDIR)
        {
            if(i==0)
            {
                fp=fopen(name_txt_path,"w");
            }
             fprintf(fp,"%s\n",files.name);
            i++;
        }
    }while(0==_findnext(File_Handle,&files));
    fclose(fp);
}

void DelFile(char *command)        //删除受管理文件
{
    char f_name[50]={0};        //文件名字
    char* svn_path=GetSvnPath();  //svn_path是svn文件夹下txt（状态表）的路径
    strcat(svn_path,"\\status.txt");
    char* ConTxt_path=GetSvnPath();  //ConTxt_path是svn文件夹下control_name.txt（受管理表）的路径
    strcat(ConTxt_path,"\\control_name.txt");
    strncpy(f_name,command+7,strlen(command)-7);

    if(IsFile(f_name)==0)
    {
        printf("This is not a file name.\n");
        return 0;
    }

    if(IsConFile(f_name)==0)
    {
        printf("this is not a controled file\n");
        return 0;
    }

    //修改status.txt的内容
    ChangeStatus(f_name,'-');
    //将文件删除出受管理列表
    FILE *ConTxt ,*newtxt;
    char *copy_path=GetSvnPath();
    strcat(copy_path,"\\tmp.txt");
    char name[50]={0};
    char copyname[50]={0};
    ConTxt=fopen(ConTxt_path,"r+");
    newtxt=fopen(copy_path,"w");
    while(fgets(name,50,ConTxt))
    {
        memset(copyname,'\0',sizeof(copyname));
        strncpy(copyname,name,strlen(name)-1);
        strrchr(copyname,' ')[0]= 0;
        if(strcmp(f_name,copyname)!=0)
        {
            fprintf(newtxt,"%s",name);
        }
    }
    if(fclose(ConTxt) != 0)
{
perror("fclose");
}
    fclose(newtxt);
    if(remove(ConTxt_path)==-1){//删除原文件
    perror("remove");}
    rename(copy_path,ConTxt_path);//将临时文件名改为原文件名

}

int IsFile(char *filename)   //判断输入的是否是一个文件，是返回1，不是返回0，错误返回-1
{
    struct _finddata_t files;
    int File_Handle;
    char buf[80];
    GetModuleFileName(NULL,buf,MAX_PATH);
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\*.*");
    File_Handle = _findfirst(buf,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return -1;
    }
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0)
        {
            if(strcmp(filename,files.name)==0)
            {
                return 1;
            }
        }
    }while(0==_findnext(File_Handle,&files));
    return 0;
}

int IsConFile(char *filename)      //判断输入的是否是受管理的一个文件，是返回1，不是返回0
{
    char* ConTxt_path=GetSvnPath();  //ConTxt_path是svn文件夹下control_name.txt（受管理表）的路径
    strcat(ConTxt_path,"\\control_name.txt");
    FILE *ConTxt;
    int IfControl=0;
    char name[50]={0};
    char copyname[50]={0};
    if(ConTxt=fopen(ConTxt_path,"r"))
    {
         while(fgets(name,50,ConTxt) != NULL)
        {
            memset(copyname,'\0',sizeof(copyname));
            strncpy(copyname,name,strlen(name)-1);
            strrchr(copyname,' ')[0]= 0;
            if(strcmp(filename,copyname)==0)
            {
                IfControl=1;
                fclose(ConTxt);
                return 1;
            }
        }
    }
    fclose(ConTxt);
    return 0;
}

int IsInStatus(char *filename)     //判断文件是否已经存在于status.txt中，是返回1，不是返回0
{
    char* path=GetSvnPath();  //path是svn文件夹下status.txt（受管理表）的路径
    strcat(path,"\\status.txt");
    FILE *fp;
    int symbol=0;
    char buf[50]={0};
    char copyname[50]={0};
    char name[50]={0};
    if(fp=fopen(path,"r"))
    {
         while(fgets(buf,50,fp) != NULL)
        {
            memset(name,'\0',sizeof(name));
            memset(copyname,'\0',sizeof(copyname));
            strncpy(copyname,buf,strlen(buf)-1);
            strncpy(name,copyname+2,strlen(copyname)-2);
            if(strcmp(filename,name)==0)
            {
                symbol=1;
                fclose(fp);
                return 1;
            }
        }
    }
    fclose(fp);
    return 0;
}

char *MD5_file (char *path, int md5_len)//获取文件md5码
{
 FILE *fp = fopen (path, "rb");
 MD5_CTX mdContext;
 int bytes;
 unsigned char data[1024];
 char *file_md5;
 int i;
 if (fp == NULL) {
  fprintf (stderr, "fopen %s failed\n", path);
  int i=GetLastError();
  printf("the style of error is %d\n",i);
  return NULL;
 }
 MD5Init (&mdContext);
 while ((bytes = fread (data, 1, 1024, fp)) != 0)
 {
  MD5Update (&mdContext, data, bytes);
 }
 MD5Final (&mdContext);

 file_md5 = (char *)malloc((md5_len + 1) * sizeof(char));
 if(file_md5 == NULL)
 {
  fprintf(stderr, "malloc failed.\n");
  return NULL;
 }
 memset(file_md5, 0, (md5_len + 1));

 if(md5_len == 16)
 {
  for(i=4; i<12; i++)
  {
   sprintf(&file_md5[(i-4)*2], "%02x", mdContext.digest[i]);
  }
 }
 else if(md5_len == 32)
 {
  for(i=0; i<16; i++)
  {
   sprintf(&file_md5[i*2], "%02x", mdContext.digest[i]);
  }
 }
 else
 {
  fclose(fp);
  free(file_md5);
  return NULL;
 }

 fclose (fp);
 return file_md5;
}

int Compare(char*filename)    //判断文件md5码是否改变,保存新的md5，改变status.txt的值
{
    char* ConTxt_path=GetSvnPath();  //ConTxt_path是svn文件夹下control_name.txt（受管理表）的路径
    strcat(ConTxt_path,"\\control_name.txt");
    FILE *ConTxt;
    int IfEqual=-1;
    long i=0;
    char name[50]={0};
    char copyname[50]={0};
    char md5[50]={0};


    char *newmd5;
    char* file_path=GetSvnPath();  //file_path是文件的路径
    strrchr(file_path, '\\')[0]= 0;
    strcat(file_path,"\\");
    strcat(file_path,filename);
    newmd5=MD5_file(file_path,32);


    if(ConTxt=fopen(ConTxt_path,"r+"))
    {
         while(fgets(name,50,ConTxt) != NULL)
        {
            memset(copyname,'\0',sizeof(copyname));
            strncpy(copyname,name,strlen(name)-1);
            strrchr(copyname,' ')[0]= 0;
            strncpy(md5,name+strlen(copyname)+1,32);
            if(strcmp(filename,copyname)==0)
            {
                if(strcmp(md5,newmd5)==0)
                {

                    IfEqual=1;
                    fclose(ConTxt);
                    return 1;
                }
                else
                {
                    fseek(ConTxt,i+strlen(filename)+1,SEEK_SET);
                    fprintf(ConTxt,newmd5);
                    fclose(ConTxt);
                    IfEqual=0;
                    return 0;
                }
            }
            i=ftell(ConTxt);
        }
    }
    fclose(ConTxt);
    return 0;
}

int Commit(char *command)      //执行commit命令
{
    //***********获取日志信息并检查输入命令是否正确*******************
    char symbol[50]={0};
    char name[50]="NULL";
    if(strlen(command)!=6)
    {
        strncpy(symbol,command+6,strlen(command)-6);
        if(symbol[0] != ' ' || symbol[1] != '"' || symbol[strlen(symbol)-1] != '"')
            {
                printf("wrong input parameter\n");
                return 0;
            }
       strncpy(name,symbol+2,strlen(symbol)-3);
    }
    memset(symbol,'\0',sizeof(symbol));

    //***************判断是否有文件修改过**********************
    int Ifchange=0;
    char tmp_buf[30];       //临时存一下status的信息
    char *buf=GetSvnPath();
    strcat(buf,"\\status.txt");
    FILE *fp;
    fp=fopen(buf,"r");
    while(fgets(tmp_buf,30,fp))
    {
        if(tmp_buf[0] != 'N'&& tmp_buf[0] != '?')
        {
            Ifchange=1;
        }
    }
    fclose(fp);
    if(Ifchange==0)
    {
        printf("no modification\n");
        return 0;
    }


    //************修改version.txt的信息************************
    int version_number;
    version_number=GetVersionNumber('f');
    buf=GetSvnPath();
    strcat(buf,"\\version.txt");
    int i=0;
    FILE *version;
    version=fopen(buf,"r");
    while(fgets(symbol,50,version) != NULL)
    {
        i++;
    }
    fclose(version);
    version=fopen(buf,"a+");
    fprintf(version,"%d %s %d\n",i,name,version_number);
    fclose(version);

    //**************把当前版本信息存入version文件夹***************
    buf=GetSvnPath();
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\version");
    char i_char[10];            //把版本序号转为字符串型
    sprintf(i_char,"%d",i);
    strcat(buf,i_char);
    mkdir(buf);                 //buf是version文件夹的路径

    char *file_path;
    file_path=GetSvnPath();
    PutInVersion(file_path,buf);    //将文件信息导入version文件夹

//***************将status复位**************************************

    buf=GetSvnPath();
    strcat(buf,"\\status.txt");     //将status.txt复位
    FILE *status_txt ,*newtxt;
    char *copy_path=GetSvnPath();
    strcat(copy_path,"\\tmp.txt");
    memset(name,'\0',sizeof(name));
    char copyname[50]={0};
    status_txt=fopen(buf,"r+");
    newtxt=fopen(copy_path,"w");
    while(fgets(name,50,status_txt))
    {
        if(name[0] != 'G' && name[0] != '-')    //这两种情况都被删掉了
        {
            if(name[0]=='?')
            {
                fprintf(newtxt,"%s",name);
            }
            else
            {
                name[0]='N';
                fprintf(newtxt,"%s",name);
            }
        }
    }
    fclose(status_txt);
    fclose(newtxt);
    remove(buf);//删除原文件
    rename(copy_path,buf);//将临时文件名改为原文件名


    buf=GetSvnPath();
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\version");
    strcat(buf,i_char);
    file_path=GetSvnPath();
    strcat(file_path,"\\anything");
    PutInVersion(file_path,buf);    //将日志信息导入version文件夹

    //×××××××××××××××××重写日志信息×××××××××××××××××××××××××××××××××
    //control不变，将name重写
   Txtname();
    //修改version_hold.txt
    int from=0;
    from=GetVersionNumber('n');
    i=i;
    Version_Hold_Update(i,from);
}

void PutInVersion(char * file_path,char *version_path)   //把文件夹中的版本文件和信息导入version目录
{
    struct _finddata_t files;
    int File_Handle;
    char *copy_path;
    copy_path=GetSvnPath();                 //copypath=...\svn
    strrchr(file_path, '\\')[0]= 0;         //version_path=...\version(i)
    strcat(file_path,"\\*.*");              //file_path=...\svn\*.*
    File_Handle = _findfirst(file_path,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0 && files.attrib != _A_SUBDIR && strcmp(files.name,"version.txt")!=0 && strcmp(files.name,"version_hold.txt")!=0)
        {
            if(IsConFile(files.name)==0 && GetFileStatus(files.name)=='-')//如果文件状态为‘-’则应删除文件
            {
                strrchr(file_path, '\\')[0]= 0;
                strcat(file_path,"\\");
                strcat(file_path,files.name);
                remove(file_path);
            }
            else
            {
            //printf("%s\n",version_path);//version_path是新文件的路径（即version里的路径）
            strcat(version_path,"\\");
            strcat(version_path,files.name);

            strrchr(file_path, '\\')[0]= 0;//file_path是当前被copy的文件的绝对路径
            strcat(file_path,"\\");
            strcat(file_path,files.name);

            strrchr(copy_path, '\\')[0]= 0;//copy_path是临时复制文件的路径
            strcat(copy_path,"\\");
            strcat(copy_path,"tmp");

            //printf("%s %s %s\n",file_path,copy_path,version_path);
            CopyFile(file_path,copy_path,TRUE);
            rename(copy_path,version_path);

            strrchr(version_path, '\\')[0]= 0;
            }
        }
    }while(0==_findnext(File_Handle,&files));
}

void PutOutVersion(char *version_path)   //把相应version文件夹里的内容取出来放到相应位置
{
    struct _finddata_t files;
    int File_Handle;
    char copy_path[100]={0};
    strcat(copy_path,version_path);
    strcat(copy_path,"\\");             //copy_path=...\version(i)\(filename)
    char *file_path;
    file_path=GetSvnPath();
    strcat(file_path,"\\");             //file_path=...\svn\(filename)
    strcat(version_path,"\\*.*");       //version_path=...\version(i)\*.*
    File_Handle = _findfirst(version_path,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.')
        {
            if(strcmp(files.name,"status.txt")==0 || strcmp(files.name,"control_name.txt")==0 || strcmp(files.name,"name.txt")==0)
            {
                file_path=GetSvnPath();
                strcat(file_path,"\\");
                strcat(file_path,files.name);

                strrchr(copy_path, '\\')[0]= 0;
                strcat(copy_path,"\\");
                strcat(copy_path,"tmp");

                strrchr(version_path, '\\')[0]= 0;
                strcat(version_path,"\\");
                strcat(version_path,files.name);

                CopyFile(version_path,copy_path,TRUE);
                rename(copy_path,file_path);

            }
            else
            {
                file_path=GetSvnPath();
                strrchr(file_path, '\\')[0]= 0;
                strcat(file_path,"\\");
                strcat(file_path,files.name);

                strrchr(copy_path, '\\')[0]= 0;
                strcat(copy_path,"\\");
                strcat(copy_path,"tmp");

                strrchr(version_path, '\\')[0]= 0;
                strcat(version_path,"\\");
                strcat(version_path,files.name);

                CopyFile(version_path,copy_path,TRUE);
                rename(copy_path,file_path);
            }
        }
    }while(0==_findnext(File_Handle,&files));

}

char GetFileStatus(char *filename) //获取文件在status里的状态
{
    char* svn_path=GetSvnPath();  //svn_path是svn文件夹下txt（状态表）的路径
    strcat(svn_path,"\\status.txt");
    FILE *sta_txt;
    sta_txt=fopen(svn_path,"r");
    int sym=0;
    char sta;
    char buffer[64]={0};
    char copybuffer[64]={0};
    while(fgets(buffer, 64, sta_txt) != NULL)
    {
        memset(copybuffer,'\0',sizeof(copybuffer));
        strncpy(copybuffer,buffer,strlen(buffer)-1);
        strcpy(copybuffer,copybuffer+2);
        if(strcmp(copybuffer,filename)==0)
        {
            sta=buffer[0];
            sym=1;
            fclose(sta_txt);
            return sta;
        }
    }
    if(sym==0)
    {
        //printf("can't find such file in the status.txt \n");
        fclose(sta_txt);
        return 'C';
    }
}

int Update(char *command,int sym)         //更新版本
{
    if(strcmp(command,"update")!=0)
    {
    //*************判断是否输入正确***************************
    //printf("%s\n",command);
    int number_int;
    char symbol[50];
    strncpy(symbol,command+6,strlen(command)-6);
    if(symbol[0] != ' '||atoi(symbol)==0)
    {
        printf("wrong input parameter\n");
        return 0;
    }
    memset(symbol,'\0',sizeof(symbol));
    strncpy(symbol,command+7,strlen(command)-7);
    number_int=atoi(symbol);
    char number_char[5];
    itoa(number_int,number_char,10);
    //printf("%s\n",symbol);

    //**************判断是否有相应的版本*****************************
    int IfGet=0;
    char copyname[50]={0};
    char filename[50]={0};
    struct _finddata_t files;
    int File_Handle;
    char *file_path=GetSvnPath();
    strrchr(file_path, '\\')[0]= 0;
    strcat(file_path,"\\*.*");
    File_Handle = _findfirst(file_path,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.' && files.attrib == _A_SUBDIR && strncmp(files.name,"version",7)==0)
        {
            strncpy(copyname,files.name+7,strlen(files.name)-7);
            //printf("%s\n%s\n",symbol,copyname);
            if(strcmp(symbol,copyname)==0)
            {
                IfGet=1;
                strcat(filename,files.name);
            }
        }
    }while(0==_findnext(File_Handle,&files));
    if(IfGet==0)
    {
        printf("no such version\n");
        return 0;
    }
    //printf("%s\n",filename);
    //****************判断是否能update************************
    char *buf=GetSvnPath();
    strcat(buf,"\\status.txt");
    char name[50]={0};
    int IfExit=0;
    if(sym==0){
    FILE *status_txt;
    status_txt=fopen(buf,"r");
    while(fgets(name,50,status_txt))
    {
        if(name[0] == '+' || name[0] == '-' || name[0] == 'G' || name[0] == 'M')
        {
            printf("there changes,update failed\n");
            fclose(status_txt);
            return 0;
        }
    }
    fclose(status_txt);}

    //****************将uptade版本里的东西拿出来***********************************
    //先将原来的都删掉
    buf=GetSvnPath();
    DelAllFile(buf);
    buf=GetSvnPath();
    strcat(buf,"\\*.*");
    DelAllFile(buf);

    file_path=GetSvnPath();
    strrchr(file_path, '\\')[0]= 0;
    strcat(file_path,"\\");
    strcat(file_path,filename);
    PutOutVersion(file_path); //注意file_path已经修改了，下次调用请重新复制

    Version_Hold_Update(number_int,number_int);
    }
    else
    {
        char number[50]={0};
        char command[50]="update ";
        itoa(GetVersionNumber('n'),number,10);
        strcat(command,number);
        Update(command,0);
    }
}

int DelAllFile(char * buf)    //删除path路径下所有非系统文件（目录、svn.exe、version.txt）
{
    struct _finddata_t files;
    int File_Handle;
    strrchr( buf, '\\')[0]= 0;
    strcat(buf,"\\*.*");
    File_Handle = _findfirst(buf,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0 && files.attrib != _A_SUBDIR &&strcmp(files.name,"version.txt")!=0 &&strcmp(files.name,"version_hold.txt")!=0)
        {
            strrchr( buf, '\\')[0]= 0;
            strcat(buf,"\\");
            strcat(buf,files.name);
            remove(buf);
        }
    }while(0==_findnext(File_Handle,&files));

    buf=GetSvnPath();
    strcat(buf,"\\*.*");
    File_Handle = _findfirst(buf,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return 0;
    }
    do
    {
        if(files.name[0]!='.' && strcmp(files.name,"svn_test.exe")!=0 && files.attrib != _A_SUBDIR &&strcmp(files.name,"version.txt")!=0)
        {
            strrchr( buf, '\\')[0]= 0;
            strcat(buf,"\\");
            strcat(buf,files.name);
            remove(buf);
        }
    }while(0==_findnext(File_Handle,&files));
}

int IsFile_svn(char *filename)      //判断输入的文件名是否存在于svn文件夹里，是返回1，不是返回0，错误返回-1
{
    struct _finddata_t files;
    int File_Handle;
    char *buf;
    buf=GetSvnPath();
    strcat(buf,"\\*.*");
    File_Handle = _findfirst(buf,&files);
    if(File_Handle==-1)
    {
        printf("error\n");
        return -1;
    }
    do
    {
        if(files.name[0]!='.')
        {
            if(strcmp(filename,files.name)==0)
            {
                return 1;
            }
        }
    }while(0==_findnext(File_Handle,&files));
    return 0;
}

int Version_Hold_Update(int i,int from)    //更新当前处于哪个版本以及从那个版本来
{
    char *path=GetSvnPath();
    char number_now[5];
    char number_from[5];
    itoa(i,number_now,10);
    itoa(from,number_from,10);
    strcat(path,"\\version_hold.txt");
    FILE *fp;
    fp=fopen(path,"w+");
    fprintf(fp,"%s %s",number_now,number_from);
    fclose(fp);
}

int GetVersionNumber(char c)      //获得当前版本号,-1表示错误
{
    int number=-1;
    char *path=GetSvnPath();
    strcat(path,"\\version_hold.txt");
    FILE *fp;
    fp=fopen(path,"r");
    char buf[10]={0};
    fgets(buf,10,fp);
    fclose(fp);
    if(c=='n')
    {
        number=atoi(buf);
    }
    char *tmp;
    char last[10]={0};
    if(c=='f')
    {
        tmp=strrchr(buf,' ');
        sprintf(last,"%s",tmp+1);
        number=atoi(last);
    }
    return number;
}

void Revert()
{
    int number=-1;
    char *path=GetSvnPath();
    strcat(path,"\\version_hold.txt");
    FILE *fp;
    fp=fopen(path,"r");
    char buf[10]={0};
    fgets(buf,10,fp);
    fclose(fp);
    int i=0;
    for(i=0;buf[i]!=' ';i++);
    char true_buf[10];
    strncpy(true_buf,buf+i+1,strlen(buf)-i-1);
    number=atoi(true_buf);
    itoa(number,true_buf,10);
    char command[50]="update ";
    strcat(command,true_buf);
    Update(command,1);
}

int log(char *command)
{
    if(strcmp(command,"log") !=0 )
    {
        int number_int;
        char symbol[50];
        strncpy(symbol,command+3,strlen(command)-3);
        if(symbol[0] != ' '||atoi(symbol)==0)
        {
            printf("wrong input parameter\n");
            return 0;
        }
        memset(symbol,'\0',sizeof(symbol));
        strncpy(symbol,command+4,strlen(command)-4);
        number_int=atoi(symbol);
        char number_char[5];
        itoa(number_int,number_char,10);

        //**************判断是否有相应的版本*****************************
        int IfGet=0;
        char copyname[50]={0};
        char filename[50]={0};
        struct _finddata_t files;
        int File_Handle;
        char *file_path=GetSvnPath();
        strrchr(file_path, '\\')[0]= 0;
        strcat(file_path,"\\*.*");
        File_Handle = _findfirst(file_path,&files);
        if(File_Handle==-1)
        {
            printf("error\n");
            return 0;
        }
        do
        {
            if(files.name[0]!='.' && files.attrib == _A_SUBDIR && strncmp(files.name,"version",7)==0)
            {
                strncpy(copyname,files.name+7,strlen(files.name)-7);
                if(strcmp(symbol,copyname)==0)
                {
                    IfGet=1;
                    strcat(filename,files.name);
                }
            }
        }while(0==_findnext(File_Handle,&files));
        if(IfGet==0)
        {
            printf("no such version\n");
            return 0;
        }
        //**********************打印版本信息**************************************
        char *version_path=GetSvnPath();
        strcat(version_path,"\\");
        strcat(version_path,"version.txt");
        FILE *fp;
        fp=fopen(version_path,"r");
        char buf[100]={0};
        char message[100]={0};
        while(fgets(buf,100,fp)!=NULL)
        {
            strrchr(buf,' ')[0]= 0;
            strncpy(message,buf,strlen(buf));
            strrchr(buf,' ')[0]= 0;
            if(strcmp(buf,symbol)==0)
            {
                printf("version:%s\n",message);
                fclose(fp);
            }
            memset(message,'\0',sizeof(message));
        }
    }
    else
    {
        char *message[100]={0};
        char *version_path=GetSvnPath();
        strcat(version_path,"\\");
        strcat(version_path,"version_hold.txt");
        FILE *version_hold;
        version_hold=fopen(version_path,"r");
        char number_char[10]={0};
        char *number_char_copy;
        fgets(number_char,10,version_hold);
        fclose(version_hold);
        strrchr(number_char, ' ')[0]= 0;
        int number_int=atoi(number_char);
        int i=0;
        while(number_int !=0)
        {
            version_path=GetSvnPath();
            strcat(version_path,"\\");
            strcat(version_path,"version.txt");
            FILE *fp;
            fp=fopen(version_path,"r");
            char buf[100]={0};
            char copybuf[100]={0};
            char *tmp;
            char last[100];
            while(fgets(buf,100,fp)!=NULL)
            {
                tmp=strrchr(buf,' ');
                sprintf(last,"%s",tmp+1);
                strrchr(buf,' ')[0]= 0;
                strncpy(copybuf,buf,strlen(buf));
                strrchr(buf,' ')[0]= 0;
                if(strcmp(buf,number_char)==0)
                {
                    if(i==0)
                    {
                        strcat(copybuf,"(当前版本)");
                    }
                    number_int=atoi(last);
                    itoa(number_int,number_char,10);
                    message[i]= (char*)malloc(sizeof(char) * 50);
                    sprintf(message[i],"%s",copybuf);
                    i++;
                    fclose(fp);
                }
                memset(copybuf,'\0',sizeof(copybuf));
                memset(last,'\0',sizeof(last));
            }
        }
        for(1;i>=0;i--)
        {
            printf("%s\n",message[i]);
            free(message[i]);
        }
    }
}

int Attribute(char *command)
{
    if(strcmp(command,"attribute") !=0 )
    {
        int number_int;
        char symbol[50];
        strncpy(symbol,command+9,strlen(command)-9);
        if(symbol[0] != ' '||atoi(symbol)==0)
        {
            printf("wrong input parameter\n");
            return 0;
        }
        memset(symbol,'\0',sizeof(symbol));
        strncpy(symbol,command+10,strlen(command)-10);
        number_int=atoi(symbol);
        char number_char[5];
        itoa(number_int,number_char,10);
        //**************判断是否有相应的版本*****************************
        int IfGet=0;
        char copyname[50]={0};
        char filename[50]={0};
        struct _finddata_t files;
        int File_Handle;
        char *file_path=GetSvnPath();
        strrchr(file_path, '\\')[0]= 0;
        strcat(file_path,"\\*.*");
        File_Handle = _findfirst(file_path,&files);
        if(File_Handle==-1)
        {
            printf("error\n");
            return 0;
        }
        do
        {
            if(files.name[0]!='.' && files.attrib == _A_SUBDIR && strncmp(files.name,"version",7)==0)
            {
                strncpy(copyname,files.name+7,strlen(files.name)-7);
                if(strcmp(symbol,copyname)==0)
                {
                    IfGet=1;
                    strcat(filename,files.name);
                }
            }
        }while(0==_findnext(File_Handle,&files));
        if(IfGet==0)
        {
            printf("no such version\n");
            return 0;
        }
        //**********************打印版本信息**************************************
        char *version_path=GetSvnPath();
        strcat(version_path,"\\");
        strcat(version_path,"version.txt");
        FILE *fp;
        fp=fopen(version_path,"r");
        char buf[100]={0};
        char message[100]={0};
        while(fgets(buf,100,fp)!=NULL)
        {
            strrchr(buf,' ')[0]= 0;
            strncpy(message,buf,strlen(buf));
            strrchr(buf,' ')[0]= 0;
            if((strcmp(buf,symbol)==0)&&IsConFile(buf) == 1)
            {
                printf("version:%s\n",message);
                fclose(fp);
            }
            memset(message,'\0',sizeof(message));
        }
        int i=0;
        char *statxt_path=GetSvnPath();
        strrchr(statxt_path, '\\')[0]= 0;
        strcat(statxt_path,"\\");
        strcat(statxt_path,filename);
        strcat(statxt_path,"\\status.txt");
        FILE *statxt;
        statxt=fopen(statxt_path,"r");
        memset(copyname,'\0',sizeof(copyname));
        memset(filename,'\0',sizeof(filename));
        while(fgets(copyname,50,statxt)!= NULL)
        {
            strncpy(filename,copyname+2,strlen(copyname)-2);
            printf("%s",filename);
            memset(filename,'\0',sizeof(filename));
            i++;
        }
        printf("find %d file\n",i);
        fclose(statxt);
    }
    else
    {
        char *message[100]={0};
        char *version_path=GetSvnPath();
        strcat(version_path,"\\");
        strcat(version_path,"version_hold.txt");
        FILE *version_hold;
        version_hold=fopen(version_path,"r");
        char number_char[10]={0};
        char *number_char_copy;
        fgets(number_char,10,version_hold);
        fclose(version_hold);
        strrchr(number_char, ' ')[0]= 0;
        char command[50]="version ";
        strcat(command,number_char);
        printf("%s\n",command);
        char copyname[50]={0};
        char filename[50]={0};
        int i=0;
        char *statxt_path=GetSvnPath();
        strcat(statxt_path,"\\status.txt");
        FILE *statxt;
        statxt=fopen(statxt_path,"r");
        memset(copyname,'\0',sizeof(copyname));
        memset(filename,'\0',sizeof(filename));
        while(fgets(copyname,50,statxt)!= NULL)
        {
            strncpy(filename,copyname+2,strlen(copyname)-2);
            printf("%s",filename);
            memset(filename,'\0',sizeof(filename));
            i++;
        }
        printf("find %d file\n",i);
        fclose(statxt);
    }
}
void DelConFile(char *command)
{
    char f_name[50]={0};        //文件名字
    char* ConTxt_path=GetSvnPath();  //ConTxt_path是svn文件夹下control_name.txt（受管理表）的路径
    strcat(ConTxt_path,"\\control_name.txt");
    strncpy(f_name,command+7,strlen(command)-7);

    //将文件删除出受管理列表
    FILE *ConTxt ,*newtxt;
    char *copy_path=GetSvnPath();
    strcat(copy_path,"\\tmp.txt");
    char name[50]={0};
    char copyname[50]={0};
    ConTxt=fopen(ConTxt_path,"r+");
    newtxt=fopen(copy_path,"w");
    while(fgets(name,50,ConTxt))
    {
        memset(copyname,'\0',sizeof(copyname));
        strncpy(copyname,name,strlen(name)-1);
        strrchr(copyname,' ')[0]= 0;
        if(strcmp(f_name,copyname)!=0)
        {
            printf("%s\n",copyname);
            fprintf(newtxt,"%s",name);
        }
    }
    fclose(ConTxt);
    fclose(newtxt);
    remove(ConTxt_path);//删除原文件
    rename(copy_path,ConTxt_path);//将临时文件名改为原文件名
}
