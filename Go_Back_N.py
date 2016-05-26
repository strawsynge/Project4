#coding:utf-8
import wx
import matplotlib
import numpy
matplotlib.use('WXAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.animation as animation
from matplotlib.figure import Figure

#------------------------图形界面GUI------------------------
class myapp(wx.App):
	def __init__(self):
		super(myapp,self).__init__(False)
		self.frame=mainframe(None,"Go-Back-N")
		self.frame.Show()


class paintpanel(wx.Panel):
	def __init__(self,parent):
		wx.Panel.__init__(self,parent,-1,size=(650,500))
		self.figure=Figure()

		# self.delay=3
		# self.n=1
		# self.lens=0.5 # step size of packet in every frame


		self.pos=[] # vertical distance of packet ongoing
		self.index=[] # horizontal location of packet ongoing
		self.remindex = []
		self.rempos = []
		# self.figure=plt.figure()
		self.axes=self.figure.add_subplot(111)
		self.canv=FigureCanvas(self,wx.ID_ANY,self.figure)
		self.axes.plot()
		#--------plot figure and animation-----------
		# for i in range(100):
		# 	self.axes.clear() 
		# 	self.animate(i)
		# self.axes.show()

	# def staticfig(self):
	# 	listt=[]
	# 	for index in range(0,20):
	# 		tmprect=plt.Rectangle((index,-0.5),1,1,fc='r')
	# 		tmprect2=plt.Rectangle((index,9.5),1,1,fc='r')
	# 		listt.append(tmprect)
	# 		listt.append(tmprect2)
	# 	for item in listt:
	# 		self.axes.add_patch(item)
	def startAnimation(self):
		# print 'ss'
		# self.axes.clear()
		frame=self.frame
		self.ani=animation.FuncAnimation(self.figure,self.animate,frames=frame,interval=100,repeat=False)

		self.sumlen=10 # distance between sender and receiver
		self.lens=2*self.sumlen/self.delay # loc change of packet between two frames

	def circle(self,index,posi,color):
		lens=2*self.sumlen/self.delay
		if posi==-1:
			return 0
		if posi>int(self.sumlen/lens):
			posi=2*int(self.sumlen/lens)-posi
			color='g'
		tmp=plt.Circle((0.5+index,posi*lens),0.25,fc=color)
		# tmprect=plt.Rectangle((first+n,-0.5),1,0.5,fc='r')
		self.axes.add_patch(tmp)
		# self.axes.add_patch(tmprect)
	

	def animate(self,i):
		n=self.n # window size
		delay=self.delay/n # time between two sended packets
		# lens=2*self.sumlen/self.delay
		# lens=self.lens # loc change of packet between two frames
		timeout=self.timeout # timeout
		self.sumlen=10 # distance between sender and receiver
		self.axes.clear() 
		listt=[] 
		# remindex = []
		# rempos = []


		# now the index is(first)
		# now we have nuni package
		# print sumlen/lens
		# %----------------------
		# %----------------------
		# %----------------------
		poplist=[]
		applist=[]
		if i==0:
			if len(self.index)==0:
				self.index.append(0)
				self.pos.append(0)
		else:
			if len(self.remindex)>0:
				for k in range(len(self.remindex)):
					tmppoplist=[]
					for p in range(len(self.rempos[k])):
						if self.rempos[k][p]<2*int(self.sumlen/self.lens):
							self.rempos[k][p]+=1
						else:
							tmppoplist.append(p)
					for p in range(len(tmppoplist)):
						self.rempos[k].pop(tmppoplist[len(tmppoplist)-1-p])

				tmppopout=[]
				for k in range(len(self.remindex)):
					if self.rempos[k]==[]:
						tmppopout.append(k)
				for k in range(len(tmppopout)):
					self.rempos.pop(tmppopout[len(tmppopout)-1-k])
					self.remindex.pop(tmppopout[len(tmppopout)-1-k])
			repeat=0
			for item in range(len(self.index)):
				if self.pos[item]<2*int(self.sumlen/self.lens):
					if self.pos[item]>=timeout and (self.pos[item]-timeout)%timeout==0:
						# if self.pos[-1]%delay==0:
						# 	if len(self.index)<n:
						# 		applist.append(self.index[-1]+1)
						if self.index[item] in self.remindex:
							self.rempos[self.remindex.index(self.index[item])].append(0)
						else:
							self.remindex.append(self.index[item])
							self.rempos.append([0])
					
					if repeat==0:
						if self.pos[-1]%delay==0:
							if len(self.index)<n and (self.index[-1]+1)%n!=0:
								applist.append(self.index[-1]+1)
						repeat+=1
					self.pos[item]=self.pos[item]+1

				else:
					if (self.index[-1]+1)%n==0:
						if self.index[item]==self.index[-1]:
							poplist.append(item)
							applist.append(self.index[-1]+1)
						else:
							poplist.append(item)
					else:
						poplist.append(item)
						applist.append(self.index[-1]+1)
					# if self.pos[-1]%delay==0:
					# 	if len(self.index)<n:
					# 		applist.append(self.index[-1]+1)
					# 		print "11-"

			for item in applist:
				self.pos.append(0)
				self.index.append(item)

			for item in range(len(poplist)):
				self.pos.pop(poplist[len(poplist)-1-item])
				self.index.pop(poplist[len(poplist)-1-item])		








		# print self.index,self.pos
		# paint package and color change

		for item in range(len(self.index)):
			self.circle(self.index[item],self.pos[item],'y')
			# tmprect=plt.Rectangle((self.index[item],10),1,0.5,fc='b')
			# self.axes.add_patch(tmprect)
		for item in range(len(self.remindex)):
			for p in self.rempos[item]:
				self.circle(self.remindex[item],p,'r')
				if p==int(self.sumlen/self.lens):
					pass

		# %----------------------
		# %----------------------
		# %----------------------
		
		# other package
		# oindex=i/wait


		# if wait<2*sumlen/lens:
		# 	oindex=(i-starttime)/wait
		# 	for item in range(oindex):
		# 		tmp=(i-starttime)/wait
		# 		self.circle(index*n,itime,posi)
		print self.index[0]

		for item in range(0,self.index[0]):
			tmprect2=plt.Rectangle((item,10),1,0.5,fc='b')
			listt.append(tmprect2)
			tmprect=plt.Rectangle((item,-0.5),1,0.5,fc='r')
			listt.append(tmprect)
		for item in range(self.index[0],max(20,self.index[-1])):
			tmprect2=plt.Rectangle((item,10),1,0.5,fc='w')
			listt.append(tmprect2)
			tmprect=plt.Rectangle((item,-0.5),1,0.5,fc='r')
			listt.append(tmprect)




		
		tmprect=plt.Rectangle((self.index[0]-(self.index[0]%n),-0.7),n,0.9,fill=False)
		listt.append(tmprect)

		for item in listt:
			self.axes.add_patch(item)

		a=self.axes.plot()
		return a



class mainframe(wx.Frame):
	def __init__(self,parent,title):
		super(mainframe,self).__init__(parent=parent,title=title,size=(850,500))
		self.loadUI()


	def loadUI(self):
		self.sp=wx.SplitterWindow(self)
		self.p1=wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
		self.p2=wx.Panel(self.sp,style=wx.SUNKEN_BORDER)
		self.sp.SplitVertically(self.p1,self.p2,650) #split the window into two panels

		# p1 paint panel
		self.paint=paintpanel(self.p1)

		# p2 control panel
		self.label1=wx.StaticText(self.p2,-1,label="Window Size:",pos=(10,10))
		self.slider1=wx.Slider(self.p2,wx.SL_HORIZONTAL,pos=(10,40),minValue=1, maxValue=6)
		self.label2=wx.StaticText(self.p2,label=str(self.slider1.GetValue()),pos=(90,10))

		self.label3=wx.StaticText(self.p2,-1,label="RTT:",pos=(10,70))
		self.slider2=wx.Slider(self.p2,wx.SL_HORIZONTAL,pos=(10,100),minValue=1, maxValue=20)
		self.label4=wx.StaticText(self.p2,label=str(self.slider2.GetValue()),pos=(90,70))

		self.label5=wx.StaticText(self.p2,-1,label="Animation Frame:",pos=(10,130))
		self.slider3=wx.Slider(self.p2,wx.SL_HORIZONTAL,pos=(10,160),minValue=100, maxValue=1000)
		self.label6=wx.StaticText(self.p2,label=str(self.slider3.GetValue()),pos=(120,130))

		self.label7=wx.StaticText(self.p2,-1,label="timeout:",pos=(10,190))
		self.slider4=wx.Slider(self.p2,wx.SL_HORIZONTAL,pos=(10,220),minValue=1, maxValue=50)
		self.label8=wx.StaticText(self.p2,label=str(self.slider2.GetValue()),pos=(90,190))

		self.startbutton=wx.Button(self.p2,label="Start",pos=(30,260))
		# self.stopbutton=wx.Button(self.p2,label="Stop",pos=(30,220))


		self.slider1.Bind(wx.EVT_SCROLL,self.onSliderChange1)
		self.slider2.Bind(wx.EVT_SCROLL,self.onSliderChange2)
		self.slider3.Bind(wx.EVT_SCROLL,self.onSliderChange3)
		self.slider4.Bind(wx.EVT_SCROLL,self.onSliderChange4)


		self.startbutton.Bind(wx.EVT_BUTTON,self.onClickConfirm)
		# self.stopbutton.Bind(wx.EVT_BUTTON,self.onClickConfirm2)
		# self.inputstrbtn.Bind(wx.EVT_BUTTON,self.onClickInput)
		# self.cancelbtn.Bind(wx.EVT_BUTTON,self.onClickCancel)
		# self.slider1.Bind(wx.EVT_SCROLL,self.onSliderChange)

	def onClickConfirm(self,event):
		self.wsize=self.slider1.GetValue()
		self.paint=paintpanel(self.p1)
		self.paint.n=self.wsize
		self.paint.delay=self.slider2.GetValue()
		self.paint.frame=self.slider3.GetValue()
		self.paint.timeout=self.slider4.GetValue()
		self.paint.startAnimation()
		self.startbutton.Enable(False)
		# self.stopbutton.Enable(True)

	def onClickConfirm2(self,event):
		pass
		# self.paint.index=[]
		# self.paint.pos=[]
		# self.paint.startAnimation()
		# self.startbutton.Enable(True)


	def onSliderChange1(self,event):
		size=self.slider1.GetValue()
		self.label2.SetLabel(str(size))

	def onSliderChange2(self,event):
		size=self.slider2.GetValue()
		self.label4.SetLabel(str(size))

	def onSliderChange3(self,event):
		size=self.slider3.GetValue()
		self.label6.SetLabel(str(size))

	def onSliderChange4(self,event):
		size=self.slider4.GetValue()
		self.label8.SetLabel(str(size))


if __name__=="__main__":
	app=myapp()
	app.MainLoop()