import requests
from bs4 import BeautifulSoup
# requests isn't scraping arabic strings, so i have used pandas to get the students name and calculating the student's total result
import pandas as pd
import numpy as np


data=[]
C_Names=["ID","Name","Analysis","Heat","Stress","Elec.","Meas.","kin.","Field-1","Total","Perc.%","Grade"]

No_of_Subjects=7
total= 725
first_ip= 25001
final_ip= 25016
current_ip=first_ip
finishing=final_ip+1

while current_ip != finishing:
    # try and except to avoid any errors of connection
    try:
        print(current_ip)

        # url1 the url of the result form after choosing the year
        url1=f"http://app1.helwan.edu.eg/EngMatrya/HasasnUpMlist.asp?z_dep=%3D&z_st_name=LIKE&z_st_settingno=%3D&x_st_settingno={current_ip}&x_st_name=&z_gro=%3D&x_gro=%C7%E1%CB%C7%E4%ED%C9&x_dep=&z_sec=LIKE&x_sec=&psearch=&Submit=++++%C8%CD%CB++++"
        req1=requests.get(url1).text
        soup1=BeautifulSoup(req1,'html.parser')
        find=soup1.find("tr",{"class":"ewTableRow","onmouseover":"ew_MouseOver(this);"})
        
        # try and except to avoid non exist id
        try:
            # find2 to find the result link
            find2=find.find("a")

            # optimizing the link of the result
            url2=f"http://app1.helwan.edu.eg/EngMatrya/{str(find2)[9:-12]}"
            
            # getting the result html code
            req2=requests.get(url2).text
            
            # to get the table which contain the student name
            name_df=pd.read_html(url2)
            soup2=BeautifulSoup(req2,'html.parser')
            deg=[]
            degrees=[]
            degrees_in_int=[]
            
            # getting all tags which may contain any results of any subject
            C1_degree=soup2.find_all("td",{"align":"center","width":"100"})
            C2_degree=soup2.find_all("td",{"align":"center","width":"81"})
            for i in C1_degree:
                    find=i.find("b")
                    if len(find.text)<3 or len(find.text)==3:
                        deg.append(find.text)

            # for just getting the No. and avoid getting any other strings
            for i in C2_degree:
                find=i.find("b")
                if len(find.text)<3 or len(find.text)==3 :
                    deg.append(find.text)

            # for getting the results of the subjects for the current semester
            for i in range(No_of_Subjects):
                degrees.append(deg[i])
            
            # converting degrees from str to int to calculate the student total degree    
            for i in degrees:
                    
                    # try and except to avoid ""
                    try:
                        degrees_in_int.append(int(i))
                    except: 
                        print("Nan")
            
                
            percentage="" 

            # try and except to avoid students which hasn't any degrees   
            try:

                # calculating the percentage
                st_degrees=pd.DataFrame(degrees_in_int).sum().loc[0]
                degrees.append(st_degrees)

                percentage=st_degrees*100/total
                degrees.append(f"{round(percentage,2)}%")
            except:
                print("Nan")
                degrees.append("")
                degrees.append("")

            # getting student name
            name=name_df[1].loc[2,1]
            degrees.insert(0,name)
            degrees.insert(0,current_ip)
            data.append(degrees)
            print(degrees)

            # calculating the grade 
            if percentage>=85:
                degrees.append("??")
            elif percentage>=75:
                degrees.append("??.??")
            elif percentage>=65:
                degrees.append("??")
            elif percentage>=50:
                degrees.append("??")
            elif percentage>=40:
                degrees.append("??")
            else:
                degrees.append("??.??") 
        except:
            print("Not exist")        

        current_ip += 1
    except:
         print("error")
         breaking=input("braking and finishing? \n 1 to break \n 0 to try again")
         if breaking == "1" :
            break
try:     
    # finishing 

    # converting the list to a data frame
    df=pd.DataFrame(data,columns=C_Names)
    df.sort_values(by = "Perc.%", ascending=False, inplace=True)
    df.index=np.arange(1,len(data)+1).tolist()

    # calculate the how many student get the same grade
    gr=df["Grade"].value_counts()
    gr=pd.DataFrame(gr)
    gr.columns=["??????????"]
    print(df)

    # convert the data frame to excel file
    df.to_excel("deg.xlsx")
    gr.to_excel("gr.xlsx")
except:
    print("close the file ")
    try_again=input("to try again \n Enter 1")
    if try_again== "1":
            df.to_excel("deg.xlsx")
            gr.to_excel("gr.xlsx")
    