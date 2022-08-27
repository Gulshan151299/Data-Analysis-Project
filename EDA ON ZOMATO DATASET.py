#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv(r"C:\Users\Manas Ranjan Kar\Downloads\archive (1)\zomato.csv")


# In[3]:


df.head(3)


# In[4]:


df.columns


# In[5]:


df.info()


# In[6]:


# Droping unnecessary columns

zomato = df.drop(['url','dish_liked','phone'],axis=1)
zomato.columns


# In[7]:


# Find and remove duplicate values

zomato.duplicated().sum()
zomato.drop_duplicates(inplace=True)


# In[8]:


# Find and remove NaN values

zomato.isnull().sum()
zomato.dropna(inplace=True)


# In[9]:


zomato.info()


# In[10]:


# changing columns name

zomato = zomato.rename(columns={'approx_cost(for two people)':'cost','listed_in(type)':'type','listed_in(city)':'city'})
zomato.columns


# In[11]:


# some transformation
zomato['cost']= zomato['cost'].astype(str)
# Using lambda function for replace ',' from cost
zomato['cost'] = zomato['cost'].apply(lambda x : x.replace(',','.'))
zomato['cost'] = zomato['cost'].astype(float)
zomato.info()


# In[12]:


zomato['rate'].unique()


# In[13]:


zomato = zomato.loc[zomato.rate != 'NEW']
zomato = zomato.loc[zomato.rate != '-'].reset_index(drop=True)
remove_slash = lambda x : x.replace('/5' , '') if type(x) == np.str else x
zomato.rate = zomato.rate.apply(remove_slash).str.strip().astype('float')


# In[14]:


zomato['rate'].unique()


# In[15]:


# Adjust the column name
zomato.name = zomato.name.apply(lambda x:x.title())
zomato.online_order.replace(('Yes','No'),(True,False),inplace = True)
zomato.book_table.replace(('Yes','No'),(True,False),inplace = True)


# In[16]:


# encode the input variables
def Encode(zomato):
    for columns in zomato.columns[~zomato.columns.isin(['rate','cost','votes'])]:
        zomato[columns] = zomato[columns].factorize()[0]
    return zomato
zomato_new = Encode(zomato.copy())
zomato_new.head()


# In[17]:


# correlation between different variables
corr = zomato_new.corr(method = 'kendall')
plt.figure(figsize = (15,8))
sns.heatmap(corr,annot=True)


# ### The highest correlation is between name and address which is 0.62 which is not very much concern

# # DATA VISUALIZATION

# ##### 1. Resturants delivering food online or not

# In[18]:


sns.countplot(zomato['online_order'])
fig = plt.gcf()
plt.title('Food delivering online or not')


# #### 2. Resturant allowing table booking or not

# In[22]:


sns.countplot(zomato['book_table'])
fig = plt.gcf()
fig.set_size_inches(6,6)
plt.title('booking table or not')


# #### 3. Table booking Rate vs Rate

# In[21]:


Y = pd.crosstab(zomato['rate'],zomato['book_table'])
Y.div(Y.sum(1).astype(float),axis = 0).plot(kind = 'bar',stacked = True , color = ['indigo','violet'])
plt.title('Table booking VS Rate',fontweight = 24,fontsize = 24 )
plt.legend(loc='best')
plt.rcParams['figure.figsize'] = (12,8)
plt.show()


# ### Location

# In[23]:


sns.countplot(zomato['city'])
sns.countplot(zomato['city']).set_xticklabels(sns.countplot(zomato['city']).get_xticklabels(),rotation = 90 , ha ='right')
# fig = plt.gcf()
fig.set_size_inches = (8,8)
plt.title('Location')


# ### 4. Location vs rating

# In[33]:


loc_plt = pd.crosstab(zomato['rate'],zomato['city'])
loc_plt.plot(kind='bar',stacked = True)
plt.title('Location vs Rating' , fontsize = 12,fontweight = 'bold')
plt.ylabel('Location',fontsize = 10,fontweight = 'bold')
plt.xlabel('Rating',fontsize = 10,fontweight = 'bold')
plt.xticks(fontsize = 8 , fontweight = 'bold')
plt.yticks(fontsize =8 , fontweight = 'bold')
plt.legend().remove()


# ### 5. Resturant Type

# In[52]:


sns.countplot(zomato['rest_type'])
sns.countplot(zomato['rest_type']).set_xticklabels(sns.countplot(zomato['rest_type']).get_xticklabels(),rotation=90,ha = 'right')
fig = plt.gcf()
fig.set_size_inches(15,10)
plt.title('Resturant Type')


# ### 5. Gussian Rest type and rating

# In[44]:


loc_plt = pd.crosstab(zomato['rate'],zomato['rest_type'])
loc_plt.plot(kind='bar',stacked = True)
plt.title('Rest type - Rating' , fontsize =16,fontweight = 'bold')
plt.xlabel('Rating',fontsize=12,fontweight='bold')
plt.ylabel('Rest Type',fontsize=12,fontweight='bold')
#plt.xticks(fontsize=10,fontweight = 'bold')
#plt.yticks(fontsize=10,fontweight = 'bold')
plt.legend().remove()


# ### 6. Type of services

# In[47]:


sns.countplot(zomato['type'])
sns.countplot(zomato['type']).set_xticklabels(sns.countplot(zomato['type']).get_xticklabels(),rotation=90,ha='right')
fig = plt.gcf()
fig.set_size_inches(10,10)
plt.title('Type of service')


# ### 7. Type and Rating

# In[53]:


type_plt = pd.crosstab(zomato['rate'],zomato['type'])
type_plt.plot(kind='bar',stacked = True)
plt.title('Type - Rating' , fontsize =16,fontweight = 'bold')
plt.xlabel('Rating',fontsize=12,fontweight='bold')
plt.ylabel('Type',fontsize=12,fontweight='bold')
#plt.xticks(fontsize=10,fontweight = 'bold')
#plt.yticks(fontsize=10,fontweight = 'bold')


# ### 8. Cost of Rsturant

# In[58]:


sns.countplot(zomato['cost'])
sns.countplot(zomato['cost']).set_xticklabels(sns.countplot(zomato['cost']).get_xticklabels(),rotation=90,ha='right')
fig = plt.gcf()
fig.set_size_inches(15,8)
plt.title('Cost Of Resturant')


# ### 9. No. Of Resturants in a Location

# In[71]:


fig = plt.figure(figsize=(16,7))
loc = sns.countplot(x='location',data = zomato,palette='Set1')
loc.set_xticklabels(loc.get_xticklabels(),rotation=90,ha ='right')
plt.ylabel('Frequency',fontsize=12,fontweight='bold')
plt.xlabel('Location',fontsize=12,fontweight='bold')
plt.title('No. of Resturants In a Location',fontsize=12,fontweight='bold')


# ### 10. Resturant Type

# In[73]:


fig = plt.figure(figsize=(16,8))
rest = sns.countplot(x='rest_type',data = zomato,palette='Set1')
rest.set_xticklabels(rest.get_xticklabels(),rotation=90,ha ='right')
plt.ylabel('Frequency',fontsize=12,fontweight='bold')
plt.xlabel('Resturant Type',fontsize=12,fontweight='bold')
plt.title('Resturants Types',fontsize=12,fontweight='bold')


# ### 11. Most famous resturant chains in Bengaluru

# In[80]:


plt.figure(figsize=(16,6))
chains = zomato['name'].value_counts()[:20]
sns.barplot(x=chains,y=chains.index,palette='Set1')
plt.xlabel('Number of outlets',fontsize=12,fontweight='bold')
plt.title('Most famous resturant chain in Bengaluru',fontsize=12,fontweight='bold')


# In[ ]:




