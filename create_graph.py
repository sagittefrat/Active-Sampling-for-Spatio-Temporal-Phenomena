import pandas as pd
import os, sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

MODES= ['Random', 'Uncertainty', 'Lookahead']
waypoints='t-waypoints scheduled'
time='total_time_sec'
score='score'
expanded='nodes_expanded'
attributes=[time, 'Day', waypoints, score, expanded]
legend_location='upper right'


arg_to_plot0='Information Gain in Number of Points Scheduled'
arg_to_plot1='Information Gain in Time'
arg_to_plot2='Points Scheduled in Time'
arg_to_plot3='Points Expanded in Time'
args_to_plot = (arg_to_plot2[7:-8], arg_to_plot1[:-13], arg_to_plot3[7:-8])
ylables = (arg_to_plot2[:-8], 'Average Score[%]', arg_to_plot3[:-8])
titles =  (arg_to_plot2, arg_to_plot1, arg_to_plot3)
x_label="Time [sec]"
#ylabel=('Points-Scheduled', 'Average Score', 'Points-Expanded')
		

def main(problem_type='spirals', precent_train=0.1, time_to_reach=1800, days=5):
	time_to_reach=int(time_to_reach)
	days=int(days)
	problem_name='%s_%s_%s'%(problem_type,precent_train, time_to_reach )
	problem_folder_name=os.path.expanduser('~/thesis/results/results_%s'%(problem_name ))
	name_to_fig='%s_%s_%s'%(problem_type,precent_train[2:],time_to_reach )

	results_df_all=pd.DataFrame(columns = attributes[:-1]+ ['mode'])
	df_score_points_all=pd.DataFrame(columns = attributes[:-1]+ ['mode'])
	#problem_folder_name=os.path.abspath('./results/')	
	num_of_problems=0
	resol=30
	for file in sorted(os.listdir(problem_folder_name)):
		if os.path.isdir(file): continue
		#print(file)
		mode=file.split('_')[0]
		
		df=pd.read_csv(os.path.join(problem_folder_name, file), index_col=False, dtype = {waypoints : "float64", 'Day':'int'})[attributes]
		#df.score=df.score*100
		
			
		df['mode']=mode
		
		
		for i in range(0,time_to_reach, resol):

			df.loc[(df[time] >= i)&(df[time] < i+resol), time] = i
		
		df_score_points_all=df_score_points_all.append(df, sort=True)
	
		last_row= df.iloc[-1:]
		
		if int(last_row.total_time_sec)<(time_to_reach-100): 
			print ('not until %s: %s'%(time_to_reach-100, file))
			#continue
		df.drop(df.loc[df[time]>time_to_reach].index, inplace=True)
	
		
		if df[df[time] == 0].empty:
		
			j = df.columns.get_loc(time)
			df.iat[len(df)-1,j]=i
			df[len(df)-1, 'score']=0
			df[len(df)-1, 'waypoints']=2
			df[len(df)-1, 'expanded']=2
			

		
			
		num_of_problems+=1
				
		results_df_all=results_df_all.append(df, sort=True)
		
	print(df_score_points_all)
	print('number of problems: %s' %(num_of_problems) )
	create_graphs(results_df_all, df_score_points_all, name_to_fig)
	
	'''for day in range(days):
		df_score_points=df_score_points_all[df_score_points_all['Day']==day].copy()
		results_df=results_df_all[results_df_all['Day']==day].copy()

		name_to_fig_new='%s_day%s' %(name_to_fig, day)
		
		create_graphs(results_df, df_score_points, name_to_fig_new, False, day)'''


	gathered_df= results_df_all.copy()
	gathered_df.loc[(gathered_df["Day"] ==1), time] += 300
	gathered_df.loc[(gathered_df["Day"] ==2), time] += 600

	gathered_score_points=df_score_points_all.copy()
	gathered_score_points.loc[(gathered_score_points["Day"] ==1), time] += 300
	gathered_score_points.loc[(gathered_score_points["Day"] ==2), time] += 600
	name_to_fig=name_to_fig+'_gathered'
	create_graphs(gathered_df, gathered_score_points, name_to_fig, True)

	return results_df_all		


	
def create_graphs(results_df_all, df_score_points, name_to_fig, gathered=False, day=None):
	
	
	print(name_to_fig)
	df_score_points_rand=df_score_points[df_score_points['mode']=='random']
	df_score_points_gree=df_score_points[df_score_points['mode']=='greedy']
	df_score_points_look=df_score_points[df_score_points['mode']=='lookahead']


	res_rand=df_score_points_rand[attributes].set_index(waypoints)
	res_rand_score=res_rand.groupby(waypoints)[score].mean()
	res_gree=df_score_points_gree[attributes].set_index(waypoints)
	res_gree_score=res_gree.groupby(waypoints)[score].mean()
	res_look=df_score_points_look[attributes].set_index(waypoints)
	res_look_score=res_look.groupby(waypoints)[score].mean()
	
	plt.figure()
	'''ax=res_rand_score.plot(label=MODES[0])
	bx=res_gree_score.plot(label=MODES[1])
	cx=res_look_score.plot(label=MODES[2])'''
	res_rand_score.plot(label=MODES[0])
	res_gree_score.plot(label=MODES[1])
	res_look_score.plot(label=MODES[2])
	
	
	#plt.legend([ax, bx, cx], MODES, loc=legend_location)
	plt.legend(loc=legend_location)
	plt.xlabel('Number of Points Scheduled')
	plt.ylabel('Average Score')
	plt.title(arg_to_plot0)
	plt.savefig('%s_%s_points.png' %(args_to_plot[1], name_to_fig))
	plt.clf()


	
	for i, attr in enumerate(attributes[2:]) :
		res_rand=results_df_all[results_df_all['mode']=='random'][attributes].set_index(time)
		res_rand_attr=res_rand.groupby(time)[attr].mean()		
		res_gree=results_df_all[results_df_all['mode']=='greedy'][attributes].set_index(time)
		res_gree_attr=res_gree.groupby(time)[attr].mean()
		res_look=results_df_all[results_df_all['mode']=='lookahead'][attributes].set_index(time)
		res_look_attr=res_look.groupby(time)[attr].mean()


		plt.figure()
		ax=res_rand_attr.plot(label=MODES[0])
		bx=res_gree_attr.plot(label=MODES[1])
		cx=res_look_attr.plot(label=MODES[2])


		if gathered:
			plt.axvline(x=300, label='Day 1', color='gray', linestyle='--')
			plt.axvline(x=600, label='Day 2', color='gray', linestyle='--')

		
		plt.legend(loc=legend_location)
		plt.xlabel(x_label)
		plt.ylabel(ylables[i])
		plt.title(titles[i])
		plt.savefig('%s_%s_%s.png' %(args_to_plot[i], name_to_fig, day))
		plt.clf()
			
	


	




	
	'''ax = plt.scatter(df_score_points[df_score_points['mode']=='random'][waypoints], df_score_points[df_score_points['mode']=='random'].score, s=10, marker="s", label=MODES[0])
	bx = plt.scatter(df_score_points[df_score_points['mode']=='greedy'][waypoints], df_score_points[df_score_points['mode']=='greedy'].score, s=10, marker="o", label=MODES[1])
	cx = plt.scatter(df_score_points[df_score_points['mode']=='lookahead'][waypoints], df_score_points[df_score_points['mode']=='lookahead'].score, s=10, marker="p", label=MODES[2])

	plt.legend([ax, bx, cx], MODES, loc='upper left')
	plt.xlabel('Number of Points Scheduled')
	plt.title(arg_to_plot1)
	plt.legend(loc='upper left')
	plt.savefig('%s_%s_%s_points.png' %(arg_to_plot1, name_to_fig, day))
	plt.clf()'''

	
	'''
	res_rand=results_df[results_df['mode']=='random'][attributes].set_index(time)
	res_rand_score=res_rand.groupby(time)[score].mean()
	res_rand_waypoints=res_rand.groupby(time)[waypoints].mean()
	res_rand_expanded=res_rand.groupby(time)[expanded].mean()

	res_gree=results_df[results_df['mode']=='greedy'][attributes].set_index(time)
	res_gree_score=res_gree.groupby(time)[score].mean()
	res_gree_waypoints=res_gree.groupby(time)[waypoints].mean()
	res_gree_expanded=res_gree.groupby(time)[expanded].mean()

	res_look=results_df[results_df['mode']=='lookahead'][attributes].set_index(time)
	res_look_score=res_look.groupby(time)[score].mean()
	res_look_waypoints=res_look.groupby(time)[waypoints].mean()
	res_look_expanded=res_look.groupby(time)[expanded].mean()

	
	df_rand=pd.DataFrame( zip(res_rand_waypoints, res_rand_score, res_rand_expanded), index=res_rand_score.index, columns = attributes[2:])
	df_gree=pd.DataFrame( zip(res_gree_waypoints, res_gree_score, res_gree_expanded), index=res_gree_score.index, columns = attributes[2:])
	df_look=pd.DataFrame( zip(res_look_waypoints, res_look_score, res_look_expanded), index=res_look_score.index, columns = attributes[2:])
	
	df = pd.DataFrame(zip(df_rand.score, df_gree.score, df_look.score), index = df_rand.index, columns = MODES) 
	df.sort_index(inplace=True)
	ax=df.plot(title=arg_to_plot1)
	ax.set_xlabel(x_label)
	plt.legend(loc=legend_location)
	plt.savefig('%s_%s_%s.png' %(arg_to_plot1, name_to_fig, day))
	plt.clf()

	df = pd.DataFrame(zip(df_rand.nodes_expanded, df_gree.nodes_expanded, df_look.nodes_expanded), index = df_rand.index, columns = MODES) 
	df.sort_index(inplace=True)
	ax=df.plot(title=arg_to_plot2)
	ax.set_xlabel(x_label)
	plt.legend(loc=legend_location)
	plt.savefig('%s_%s_%s.png' %(arg_to_plot2, name_to_fig, day))
	plt.clf()

	df = pd.DataFrame(zip(df_rand[waypoints], df_gree[waypoints], df_look[waypoints]), index = df_rand.index, columns = MODES) 
	df.sort_index(inplace=True)
	ax=df.plot(title=arg_to_plot3)
	ax.set_xlabel(x_label)
	plt.legend(loc=legend_location)
	plt.savefig('%s_%s_%s.png' %(arg_to_plot3, name_to_fig, day))
	plt.clf()	

	ax = plt.scatter(df_rand[waypoints], df_rand.score, s=10, marker="s", label=MODES[0])
	bx = plt.scatter(df_gree[waypoints], df_gree.score, s=10, marker="o", label=MODES[1])
	cx = plt.scatter(df_look[waypoints], df_look.score, s=10, marker="p", label=MODES[2])
	plt.legend([ax, bx, cx], MODES, loc=legend_location)
	plt.xlabel('Number of Points Scheduled')
	plt.title(arg_to_plot1)
	plt.savefig('%s_%s_%s_points_avg.png' %(arg_to_plot1, name_to_fig, day))
	plt.clf()'''

if __name__ == '__main__':
	main( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )	
