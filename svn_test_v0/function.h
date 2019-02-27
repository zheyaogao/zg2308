#ifndef FUNCTION_H_INCLUDED
#define FUNCTION_H_INCLUDED
char *GetSvnPath();   //获取svn文件夹的路径
int Create(void);           //创建svn文件夹
int Status(void);           //维护并打印状态表（status.txt）
int Getcommand(char *command);        //获取输入的命令
int Addfile(char *command);          //修改状态表信息
int Txtname();         //维护名字表
#endif // FUNCTION_H_INCLUDED
char *GetSvnPath(void);   //获取svn文件夹的路径
int Create(void);           //创建svn文件夹,创建version.txt文件（如果没有的话）
int Status(void);           //维护并打印状态表（status.txt）
int Getcommand(char *command);        //获取输入的命令
int Addfile(char *command);           //添加受管理文件到contorl文本，并修改status文本
int Txtname();                       //name.txt用于保存当前工作区所有的文件名，每次调用会重写
void DelFile(char *command);          //删除受管理文件
int IsFile(char *filename);           //判断输入的是否是一个文件，是返回1，不是返回0，错误返回-1
int IsFile_svn(char *filename);       //判断输入的文件名是否存在于svn文件夹里，是返回1，不是返回0，错误返回-1
int IsInStatus(char *filename);       //判断文件是否已经存在于status.txt中，是返回1，不是返回0
int IsConFile(char *filename);        //判断输入的是否是受管理的一个文件，是返回1，不是返回0
char *MD5_file (char *path, int md5_len); //获取文件md5码
int Compare(char*filename);           //判断文件md5码是否改变,保存新的md5，改变status.txt的值
char GetFileStatus(char *filename);   //获取文件在status里的状态
void ChangeStatus(char *filename,char c); //修改status的标志位‘c’
int Commit(char *command);             //执行commit命令
void PutInVersion(char * file_path,char *version_path);      //把文件夹中的版本文件和信息导入version目录（因为有两个文件夹所以设个函数方便一点）
void PutOutVersion(char *version_path);                     //把相应version文件夹里的内容取出来放到相应位置
int Update(char *command,int symbol);               //更新版本
int DelAllFile(char * path);             //删除path路径下所有非系统文件（目录、svn.exe、version.txt）
int Version_Hold_Update(int now,int from);          //更新当前处于哪个版本以及从那个版本来
int GetVersionNumber(char c);                  //获得当前版本号,-1表示错误
void Revert();                            //revert
int log(char *command);                  //log
int Attribute(char *command);
void DelConFile(char *command);

