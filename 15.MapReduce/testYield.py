# coding=gbk
#由浅入深详细介绍yield以及generator

#generator基础

#1.在python的函数定义中，只要出现了yield表达式，那么事实上定义的是一个generator funcion
#调用这个generator function返回值是一个generator
def gen_generator():
	''' 
		该函数返回的是一个generator实例
	'''
	yield 1

def gen_value():
	return 1

''' generator实例：
。遵循迭代器协议，迭代器协议需要实现__iter__,next接口
。能够多次进入，多次返回，能够暂停函数体中代码的执行

'''	

'''
#测试以上两个函数的差别
ret = gen_generator()
print(ret)
print(type(ret))

ret=gen_value()
print(ret)
print(type(ret))
'''

def gen_example():
	print("before any yield")
	yield "first yeild"
	print("between yeilds")
	yield "second yeild"
	print("no yeild anymore")
'''
#调用gen_example()方法并没有输出任何内容，说明函数体的代码尚未开始执行
gen=gen_example()
#当调用generator的next方法，generator会执行到yield表达式处，
#返回yield表达式的内容，然后挂起在这个地方

#暂停意味着方法的局部变量，指针信息，运行环境都保存起来，直到下一次调用next方法恢复
gen.__next__()#第一次调用next

gen.__next__()

gen.__next__()


'''

#因为for语句能自动捕获StopIteration异常，所以generator(本质上是任何iterator)较为常用的方法是在循环中使用
def generator_example():
	yield 1
	yield 2
'''	
for e in generator_example():
	print(e)
	
#generator function产生的generator与普通的function有什么区别？
#。function每次都是从第一行开始运行，而generator从上一次yield开始的地方运行
#。function调用一次返回一个（组）值，而generator可以多次返回
#。function可以被无数次重复调用，而一个generator实例在yield最后一个值或者return之后就不能继续调用了
	
。在函数中使用yield，然后调用该函数是生成generator的一种方式
。generator expression--->生成器表达式
	eg: gen=(x*x for x in range(5) )
	
'''

#generator应用


#1.基础应用
#使用generator的最重要的原因：按需生成并返回结果，而不是一次性产生所有的返回值，况且有时候根本就不知道“所有的返回值”
rang_num=100
#对列表进行迭代
for i in [x*x for x in range(rang_num)]:
	print(i)

#对generator进行迭代
for i in (x*x for x in range(rang_num)):
	print(i)


#以下为一个可以“返回”无穷多次的例子
def fib():
	a,b=1,1
	while True:
		yield a
		a,b=b,a+b


#高级应用：
#使用场景一：Generator可用于产生数据流，generator并不立刻产生返回值，
#而是等到被需要的时候才会产生返回值，相当于一个主动拉取的过程
def gen_data_from_file(file_name):
	for line in file(file_name):
		yield line
		
def gen_words(line):
	for word in (w for w in line.split() if w.strip()):
		yield word 
		
def count_words(file_name):
	word_map={}
	for line in gen_data_from_file(file_name):
		for word in gen_words(line):
			if word not in word_map:
				word_map[word] = 0
			word_map[word] += 1
		
	return word_map
	
	
def count_total_chars(file_name):
	total=0
	for line in gen_data_from_file(file_name):
		total += len(line)
	return total   
	
	
#使用场景二：
# 一些编程场景中，一件事情可能需要执行一部分逻辑，然后等待一段时间，或者等待某个异步的结果，或者等待某个状态
#然后继续执行另一部分逻辑

#对于这种需要等待，而又不希望阻塞的情况，我们一般使用回调的方式
def do(a):
	print("do")
	print(a)
	CallBackMgr.callback(5, lambda a=a:post_do(a) )
	
def post_do(a):
	print("post_do")
	print(a)

#用yield来修改这个例子，yield返回值代表等待的时间
@yield_dec
def do(a):
	print("do "+str(a))
	yield 5
	print("post_do "+str(a))

#这里需要实现一个YieldManager,通过yield_dec这个decrator将do这个genarator注册到YieldManager，
#并在5s后调用next方法
#coding:utf-8
import sys
import types
import time

class YieldManager(object):
	def __init__(self,tick_delta=0.01):
		self.generator_dict={}
		
	def tick(self):
		cur=time.time()
		for gene, t in self.generator_dict.items():
			if cur>=t:
				self.__do__resume__generator(gene,cur)
				
	def __do__resume__genartor(self,gene,cur):
		try:
			self.on_generator_excute(gene,cur)
		except StopIteration as  e:
			self.remove_generator(gene)
		except Exception as e:
			print("unexcepte error:")
			print(type(e))
			self.remove_generator(gene)
		
	def add_generator(self,gen,deadline):
		self.generator_dict[gen]=deadline
		
	def remove_generator(self,gene):
		del self.generator_dict[gene]
		
	def on_generator_excute(self,gen,cur_time=None):
		t=gen.__next__()
		cur_time=cur_time or time.time()
		self.add_generator(gen,t+cur_time)
	
g_yield_mgr=YieldManager()

def yield_dec(func):
	def __inner_func__(*args,**kwargs):
		gen=func(*args,**kwargs)
		if type(gen) is types.GeneratorType:
			g_yield_mgr.on_generator_excute(gen)

		return gen
	
	return __inner_func__

#注意事项：
#	。Yield是不能嵌套的






































