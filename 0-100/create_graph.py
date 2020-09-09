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


def main(problem_type='spirals', precent_train=0.1, time_to_reach=1800, days=5):
	time_to_reach=int(time_to_reach)
	days=int(days)
	problem_name='%s_%s'%(problem_type,precent_train )
	name_to_fig='%s_%s'%(problem_type,precent_train[2:] )
	problem_folder_name=os.path.expanduser('~/thesis/results/results_%s'%(problem_name ))
	
	arg_to_plot1='Information-Gain'
	arg_to_plot2='Points-Scheduled'
	arg_to_plot3='Points-Expanded'
	x_label="Time [sec]"
	
	results_df_all=pd.DataFrame(columns = attributes[:-1]+ ['mode'])
	df_score_points_all=pd.DataFrame(columns = attributes[:-1]+ ['mode'])
	#problem_folder_name=os.path.abspath('./results/')	
	num_of_problems=0
	
	for file in sorted(os.listdir(problem_folder_name)):
		if os.path.isdir(file): continue
	
		
		mode=file.split('_')[0]
		
		df=pd.read_csv(os.path.join(problem_folder_name, file), index_col=False, dtype = {waypoints : "float64", 'Day':'int'})[attributes]
		#df.score=df.score*100
		
			
		df['mode']=mode
		
		
		for i in range(0,time_to_reach, 60):

			df.loc[(df[time] >= i)&(df[time] < i+60), time] = i
		
		df_score_points_all=df_score_points_all.append(df, sort=True)
	
		last_row= df.iloc[-1:]
		
		if int(last_row.total_time_sec)<(time_to_reach-100): 
			print ('not until %s: %s'%(time_to_reach-0, file))
			#continue
		df.drop(df.loc[df[time]>time_to_reach].index, inplace=True)
		

		for i in range(0,time_to_reach, 60):
			
			if df[df[time] == i].empty:
				
				#print(i, df[df[time] == i].empty)
				temp_df=df[df[time] == i-60]
				
				temp=temp_df.loc[temp_df[expanded].idxmax()]
				
				df.loc[len(df)]=temp
				j = df.columns.get_loc(time)
				df.iat[len(df)-1,j]=i
			
		
			
		num_of_problems+=1
				
		results_df_all=results_df_all.append(df, sort=True)
		
	
			
	#results_df.to_csv('all_res_%s.csv'%(name_to_fig))
	#df_score_points.to_csv('score_points_res_%s.csv'%(name_to_fig))
	print(df_score_points_all)
	
	
	'''ax = plt.scatter(df_score_points_all[df_score_points_all['mode']=='random'][waypoints], df_score_points_all[df_score_points_all['mode']=='random'].score, s=10, marker="s", label=MODES[0])
	bx = plt.scatter(df_score_points_all[df_score_points_all['mode']=='greedy'][waypoints], df_score_points_all[df_score_points_all['mode']=='greedy'].score, s=10, marker="o", label=MODES[1])
	cx = plt.scatter(df_score_points_all[df_score_points_all['mode']=='lookahead'][waypoints], df_score_points_all[df_score_points_all['mode']=='lookahead'].score, s=10, marker="p", label=MODES[2])

	plt.legend([ax, bx, cx], MODES, loc='upper left')
	plt.xlabel('Number of Points Scheduled')
	plt.title(arg_to_plot1)
	plt.legend(loc='upper left')
	plt.savefig('%s_%s_points.png' %(arg_to_plot1, name_to_fig))
	plt.clf()'''

	
	
	res_rand=results_df_all[results_df_all['mode']=='random'][attributes].set_index(time)
	res_rand_score=res_rand.groupby(time)[score].mean()
	res_rand_waypoints=res_rand.groupby(time)[waypoints].mean()
	res_rand_expanded=res_rand.groupby(time)[expanded].mean()

	res_gree=results_df_all[results_df_all['mode']=='greedy'][attributes].set_index(time)
	res_gree_score=res_gree.groupby(time)[score].mean()
	res_gree_waypoints=res_gree.groupby(time)[waypoints].mean()
	res_gree_expanded=res_gree.groupby(time)[expanded].mean()

	res_look=results_df_all[results_df_all['mode']=='lookahead'][attributes].set_index(time)
	res_look_score=res_look.groupby(time)[score].mean()
	res_look_waypoints=res_look.groupby(time)[waypoints].mean()
	res_look_expanded=res_look.groupby(time)[expanded].mean()

	
	df_rand=pd.DataFrame( zip(res_rand_waypoints, res_rand_score, res_rand_expanded), index=res_rand_score.index, columns = attributes[2:])
	df_gree=pd.DataFrame( zip(res_gree_waypoints, res_gree_score, res_gree_expanded), index=res_gree_score.index, columns = attributes[2:])
	df_look=pd.DataFrame( zip(res_look_waypoints, res_look_score, res_look_expanded), index=res_look_score.index, columns = attributes[2:])
	
	'''for i in range(0,time_to_reach, 60):
	
		if i not in df_rand.index:
			df_rand.loc[i]=df_rand.loc[i-60]
		
		
		if i not in df_gree.index:
			print( df_gree.loc[i-60])
			df_gree.loc[i]=df_gree.loc[i-60]'''
			
			
	df = pd.DataFrame(zip(df_rand.score, df_gree.score, df_look.score), index = df_rand.index, columns = MODES) 
	df.sort_index(inplace=True)
	ax=df.plot(title=arg_to_plot1)
	ax.set_xlabel(x_label)
	plt.legend(loc=legend_location)
	plt.savefig('%s_%s.png' %(arg_to_plot1, name_to_fig))
	plt.clf()

	df = pd.DataFrame(zip(df_rand.nodes_expanded, df_gree.nodes_expanded, df_look.nodes_expanded), index = df_rand.index, columns = MODES) 
	df.sort_index(inplace=True)
	ax=df.plot(title=arg_to_plot2)
	ax.set_xlabel(x_label)
	plt.legend(loc=legend_location)
	plt.savefig('%s_%s.png' %(arg_to_plot2, name_to_fig))
	plt.clf()

	df = pd.DataFrame(zip(df_rand[waypoints], df_gree[waypoints], df_look[waypoints]), index = df_rand.index, columns = MODES) 
	df.sort_index(inplace=True)
	ax=df.plot(title=arg_to_plot3)
	ax.set_xlabel(x_label)
	plt.legend(loc=legend_location)
	plt.savefig('%s_%s.png' %(arg_to_plot3, name_to_fig))
	plt.clf()	

	ax = plt.scatter(df_rand[waypoints], df_rand.score, s=10, marker="s", label=MODES[0])
	bx = plt.scatter(df_gree[waypoints], df_gree.score, s=10, marker="o", label=MODES[1])
	cx = plt.scatter(df_look[waypoints], df_look.score, s=10, marker="p", label=MODES[2])
	plt.legend([ax, bx, cx], MODES, loc=legend_location)
	plt.xlabel('Number of Points Scheduled')
	plt.title(arg_to_plot1)
	plt.savefig('%s_%s_points_avg.png' %(arg_to_plot1, name_to_fig))
	plt.clf()
	
	for day in range(days):
		df_score_points=df_score_points_all[df_score_points_all['Day']==day].copy()
		results_df=results_df_all[results_df_all['Day']==day].copy()
		
		'''ax = plt.scatter(df_score_points[df_score_points['mode']=='random'][waypoints], df_score_points[df_score_points['mode']=='random'].score, s=10, marker="s", label=MODES[0])
		bx = plt.scatter(df_score_points[df_score_points['mode']=='greedy'][waypoints], df_score_points[df_score_points['mode']=='greedy'].score, s=10, marker="o", label=MODES[1])
		cx = plt.scatter(df_score_points[df_score_points['mode']=='lookahead'][waypoints], df_score_points[df_score_points['mode']=='lookahead'].score, s=10, marker="p", label=MODES[2])

		plt.legend([ax, bx, cx], MODES, loc='upper left')
		plt.xlabel('Number of Points Scheduled')
		plt.title(arg_to_plot1)
		plt.legend(loc='upper left')
		plt.savefig('%s_%s_%s_points.png' %(arg_to_plot1, name_to_fig, day))
		plt.clf()'''

		
		
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
		plt.clf()	
		
	print('number of problems: %s' %(num_of_problems) )
	
if __name__ == '__main__':
	main( sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] )	
