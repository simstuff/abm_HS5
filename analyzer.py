import os 
import glob
import networkx as nx
import pandas as pd
import logging

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
Logger=logging.getLogger("logger")
Logger.setLevel(logging.DEBUG)

#expose trust network
#calculate per t the social influence on average
#calate per t the clustering and the importance of nodes

#load step data func needed
class Analyzer():
    def __init__(self,path:str) -> None:
        self.path=path
        self.g_paths=None
        self.a_paths=None
        self.G=None
        self.model_data=None
        self.agent_data=None  
           
    def load_graphs(self):
        path_list={}
        for i,folder in enumerate(sorted(os.listdir(self.path),key=lambda x:int(x))):
            os.chdir(self.path)
            paths=glob.glob(os.path.join(self.path,folder,'*.{}'.format("edgelist")))
            paths=sorted(paths, key = lambda x: x[-24:])
            path_list[i]=paths
            
        Logger.info("Loaded graphs.")
        return path_list
    
    def create_network(self,run:int,iteration:int):
        edgelist=self.g_paths[run][iteration]
        G=nx.read_edgelist(edgelist,create_using=nx.DiGraph)
        Logger.info("Created network {}".format(G))
        return G

    
    def load_agent_data(self):
        path_list=[]
        for folder in os.listdir(self.path):
            os.chdir(self.path)
            path_list.append(glob.glob(os.path.join(self.path,folder,'agent_data.{}'.format("csv"))))      
        Logger.info("Loaded agents.")
        return path_list



    def read_csv_t(self,paths:list,run:int):
        path="%s" % "','".join(paths[run])
        df=pd.read_csv(path)
        return df
    
    def create_degree_df(self,G:nx.DiGraph,step:int,out:bool):
        if out:
            degree_df = dict(G.out_degree(weight="weight"))
            degree_df = pd.DataFrame(degree_df, index=["out_degree"]).T
            degree_df = degree_df.reset_index()
            degree_df.rename(columns={"index":"ID"},inplace=True)
            degree_df["ID"]=degree_df["ID"].astype(int)
            degree_df["Step"]=step
        else:
            degree_df = dict(G.in_degree(weight="weight"))
            degree_df = pd.DataFrame(degree_df, index=["in_degree"]).T
            degree_df = degree_df.reset_index()
            degree_df.rename(columns={"index":"ID"},inplace=True)
            degree_df["ID"]=degree_df["ID"].astype(int)
            degree_df["Step"]=step

        return degree_df
    

    def merge_df(self,df1:pd.DataFrame,df2:pd.DataFrame):
        df=pd.merge(df1,df2,on=["Step","ID"])
        return df
    
    def create_pagerank(self, G:nx.DiGraph, step:int):
        pagerank = nx.pagerank(G)
        pagerank_df = pd.DataFrame(pagerank, index=[0]).T
        pagerank_df.columns = ['pagerank']
        pagerank_df = pagerank_df.reset_index()
        pagerank_df.rename(columns={"index":"ID"},inplace=True)
        pagerank_df["ID"]=pagerank_df["ID"].astype(int)
        pagerank_df["Step"]=step
        return pagerank_df
    
    def analyze_nodes(self):
        self.a_paths=self.load_agent_data()
        self.g_paths=self.load_graphs()

        for i in range(20):
            self.agent_data=self.read_csv_t(paths=self.a_paths,run=i)
            for j in range(100):
                G=self.create_network(i,j)
                if G is not None:
                    out_degrees = self.create_degree_df(G,j,True)
                    in_degrees = self.create_degree_df(G,j,False)
                    pagerank = self.create_pagerank(G,j)
                    self.model_data=self.merge_df(self.agent_data,out_degrees)
                    self.model_data=self.merge_df(self.model_data,in_degrees)
                    self.model_data=self.merge_df(self.model_data,pagerank)
                    self.model_data["clustering"]=nx.average_clustering(G)
                    self.model_data.to_csv(self.path+"/"+str(i+1)+"/"+str(j)+"step_data.csv")
                    Logger.info("finished {}{}".format(i,j))

    def remove_negative_edges(G:nx.DiGraph):
        edges_list=[(a,b) for a,b,c in G.edges(data=True) if c["weight"]<=0]
        G.remove_edges_from(edges_list)
        

    def load_model_data(self,step:int):
        path=self.path+"/"+str(step)+"/"+"model_data.csv"
        data=pd.read_csv(path)
        return data
    

    def analyze_network(self):
        for i in range(20):
            self.model_data=self.load_model_data(i+1)
            self.g_paths=self.load_graphs()
            clustering=[]
            n_nodes=[]
            n_edges=[]
            avg_influence=[]
            for j in range(100):
                G=self.create_network(i,j)
                if G is not None:
                    clustering.append(nx.average_clustering(G))
                    n_nodes.append(G.number_of_nodes())
                    n_edges.append(G.size())
                influence=0
                for attr in G.edges(data=True):
                    influence+=(attr[2]["info"])
                avg_influence.append(influence/len(G.edges()))   
                                     
                Logger.info("finished step: {}".format(j))
            self.model_data["avgClustering"]=pd.Series(clustering)
            self.model_data["edges"]=pd.Series(n_edges)
            self.model_data["nodes"]=pd.Series(n_nodes)
            self.model_data["avg_influence"]=pd.Series(avg_influence)
            Path=self.path+"/"+str(i+1)+"/"+"network_data.csv"
            self.model_data.to_csv(Path)
            n_nodes=[]
            n_edges=[]
            clustering=[]
            avg_influence=[]
    
    def combine_step_data(self):
        df=None
        n_df=None

        for i,folder in enumerate(sorted(os.listdir(self.path),key=lambda x:int(x))):
            os.chdir(self.path+'/{}'.format(str(i+1)))
            paths=glob.glob(os.path.join(self.path,folder,'*step_data.{}'.format("csv")))
            for path in paths:
                print(path)
                if df is None:
                    df=pd.read_csv(path)
                    df["run"]=i
                else:
                    df2=pd.read_csv(path)
                    df2["run"]=i
                    df=pd.concat([df,df2],axis=0,ignore_index=True) 
            
        Logger.info("Combined step data.")
        return df


analyzer=Analyzer(path="/home/niklas/Documents/Studium_Uni_Bamberg/Semester4/PWM-PT-HS5/data")
print(os.listdir(analyzer.path))
analyzer.g_paths=analyzer.load_graphs()
print(analyzer.g_paths[19])

df=analyzer.combine_step_data()
df.to_csv(analyzer.path+"all_data.csv")
#analyzer.combine_step_data().head()

#analyzer.G=analyzer.create_network(4,67)

# #print(analyzer.G.edges(data=True))
# av=0

# for attr in analyzer.G.edges(data=True):
#     av+=(attr[2]["info"])
#     print(av)
# av=av/len(analyzer.G.edges())
# print(len(analyzer.G.edges()))
# print(analyzer.G)
# print(av)
# #analyzer.analyze_network()

#analyzer.analyze_nodes()