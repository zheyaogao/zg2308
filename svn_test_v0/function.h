#ifndef FUNCTION_H_INCLUDED
#define FUNCTION_H_INCLUDED
char *GetSvnPath();   //��ȡsvn�ļ��е�·��
int Create(void);           //����svn�ļ���
int Status(void);           //ά������ӡ״̬��status.txt��
int Getcommand(char *command);        //��ȡ���������
int Addfile(char *command);          //�޸�״̬����Ϣ
int Txtname();         //ά�����ֱ�
#endif // FUNCTION_H_INCLUDED
char *GetSvnPath(void);   //��ȡsvn�ļ��е�·��
int Create(void);           //����svn�ļ���,����version.txt�ļ������û�еĻ���
int Status(void);           //ά������ӡ״̬��status.txt��
int Getcommand(char *command);        //��ȡ���������
int Addfile(char *command);           //����ܹ����ļ���contorl�ı������޸�status�ı�
int Txtname();                       //name.txt���ڱ��浱ǰ���������е��ļ�����ÿ�ε��û���д
void DelFile(char *command);          //ɾ���ܹ����ļ�
int IsFile(char *filename);           //�ж�������Ƿ���һ���ļ����Ƿ���1�����Ƿ���0�����󷵻�-1
int IsFile_svn(char *filename);       //�ж�������ļ����Ƿ������svn�ļ�����Ƿ���1�����Ƿ���0�����󷵻�-1
int IsInStatus(char *filename);       //�ж��ļ��Ƿ��Ѿ�������status.txt�У��Ƿ���1�����Ƿ���0
int IsConFile(char *filename);        //�ж�������Ƿ����ܹ����һ���ļ����Ƿ���1�����Ƿ���0
char *MD5_file (char *path, int md5_len); //��ȡ�ļ�md5��
int Compare(char*filename);           //�ж��ļ�md5���Ƿ�ı�,�����µ�md5���ı�status.txt��ֵ
char GetFileStatus(char *filename);   //��ȡ�ļ���status���״̬
void ChangeStatus(char *filename,char c); //�޸�status�ı�־λ��c��
int Commit(char *command);             //ִ��commit����
void PutInVersion(char * file_path,char *version_path);      //���ļ����еİ汾�ļ�����Ϣ����versionĿ¼����Ϊ�������ļ������������������һ�㣩
void PutOutVersion(char *version_path);                     //����Ӧversion�ļ����������ȡ�����ŵ���Ӧλ��
int Update(char *command,int symbol);               //���°汾
int DelAllFile(char * path);             //ɾ��path·�������з�ϵͳ�ļ���Ŀ¼��svn.exe��version.txt��
int Version_Hold_Update(int now,int from);          //���µ�ǰ�����ĸ��汾�Լ����Ǹ��汾��
int GetVersionNumber(char c);                  //��õ�ǰ�汾��,-1��ʾ����
void Revert();                            //revert
int log(char *command);                  //log
int Attribute(char *command);
void DelConFile(char *command);

