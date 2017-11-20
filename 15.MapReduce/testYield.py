# coding=gbk
#��ǳ������ϸ����yield�Լ�generator

#generator����

#1.��python�ĺ��������У�ֻҪ������yield���ʽ����ô��ʵ�϶������һ��generator funcion
#�������generator function����ֵ��һ��generator
def gen_generator():
	''' 
		�ú������ص���һ��generatorʵ��
	'''
	yield 1

def gen_value():
	return 1

''' generatorʵ����
����ѭ������Э�飬������Э����Ҫʵ��__iter__,next�ӿ�
���ܹ���ν��룬��η��أ��ܹ���ͣ�������д����ִ��

'''	

'''
#�����������������Ĳ��
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
#����gen_example()������û������κ����ݣ�˵��������Ĵ�����δ��ʼִ��
gen=gen_example()
#������generator��next������generator��ִ�е�yield���ʽ����
#����yield���ʽ�����ݣ�Ȼ�����������ط�

#��ͣ��ζ�ŷ����ľֲ�������ָ����Ϣ�����л���������������ֱ����һ�ε���next�����ָ�
gen.__next__()#��һ�ε���next

gen.__next__()

gen.__next__()


'''

#��Ϊfor������Զ�����StopIteration�쳣������generator(���������κ�iterator)��Ϊ���õķ�������ѭ����ʹ��
def generator_example():
	yield 1
	yield 2
'''	
for e in generator_example():
	print(e)
	
#generator function������generator����ͨ��function��ʲô����
#��functionÿ�ζ��Ǵӵ�һ�п�ʼ���У���generator����һ��yield��ʼ�ĵط�����
#��function����һ�η���һ�����飩ֵ����generator���Զ�η���
#��function���Ա��������ظ����ã���һ��generatorʵ����yield���һ��ֵ����return֮��Ͳ��ܼ���������
	
���ں�����ʹ��yield��Ȼ����øú���������generator��һ�ַ�ʽ
��generator expression--->���������ʽ
	eg: gen=(x*x for x in range(5) )
	
'''

#generatorӦ��


#1.����Ӧ��
#ʹ��generator������Ҫ��ԭ�򣺰������ɲ����ؽ����������һ���Բ������еķ���ֵ��������ʱ������Ͳ�֪�������еķ���ֵ��
rang_num=100
#���б���е���
for i in [x*x for x in range(rang_num)]:
	print(i)

#��generator���е���
for i in (x*x for x in range(rang_num)):
	print(i)


#����Ϊһ�����ԡ����ء������ε�����
def fib():
	a,b=1,1
	while True:
		yield a
		a,b=b,a+b


#�߼�Ӧ�ã�
#ʹ�ó���һ��Generator�����ڲ�����������generator�������̲�������ֵ��
#���ǵȵ�����Ҫ��ʱ��Ż��������ֵ���൱��һ��������ȡ�Ĺ���
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
	
	
#ʹ�ó�������
# һЩ��̳����У�һ�����������Ҫִ��һ�����߼���Ȼ��ȴ�һ��ʱ�䣬���ߵȴ�ĳ���첽�Ľ�������ߵȴ�ĳ��״̬
#Ȼ�����ִ����һ�����߼�

#����������Ҫ�ȴ������ֲ�ϣ�����������������һ��ʹ�ûص��ķ�ʽ
def do(a):
	print("do")
	print(a)
	CallBackMgr.callback(5, lambda a=a:post_do(a) )
	
def post_do(a):
	print("post_do")
	print(a)

#��yield���޸�������ӣ�yield����ֵ����ȴ���ʱ��
@yield_dec
def do(a):
	print("do "+str(a))
	yield 5
	print("post_do "+str(a))

#������Ҫʵ��һ��YieldManager,ͨ��yield_dec���decrator��do���genaratorע�ᵽYieldManager��
#����5s�����next����
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

#ע�����
#	��Yield�ǲ���Ƕ�׵�






































