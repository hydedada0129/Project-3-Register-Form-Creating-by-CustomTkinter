import json
import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk


FILE_PATH = 'my_form.json'

#login frame(class)
class FormLogin(ttk.Frame):
    def __init__(self, root, data, **kwargs):
        super().__init__(root, **kwargs)
        self.mail_label = tk.Label(self, text='Email address')
        self.mail_label.pack()

        # entering your data and then set/update it dynamically by using the "textvariable" param
        self.mail_entry = tk.Entry(self, textvariable=data['mail'])    # Entry() <---> data{} , connectiing each other.
        self.mail_entry.pack()
        
        self.id_label = tk.Label(self, text='Account ID')
        self.id_label.pack()
        self.id_entry = tk.Entry(self, textvariable=data['id'])
        self.id_entry.pack()
        
        self.pw_label = tk.Label(self, text='Password')
        self.pw_label.pack()
        self.pw_entry = tk.Entry(self, show='*', textvariable=data['pw'])
        self.pw_entry.pack()
        
#
class FormGender(ttk.Frame):
    def __init__(self, root, data, **kwargs):
        super().__init__(root,**kwargs)
        self.m = ttk.Radiobutton(self, text='male',
                                 variable=data['gen'],
                                 value='m')
        self.m.pack(side='left')
        self.f = ttk.Radiobutton(self, text='female',
                                 variable=data['gen'],
                                 value='f')
        self.f.pack(side='left')
        self.o = ttk.Radiobutton(self, text='others',
                                 variable=data['gen'],
                                 value='o')
        self.o.pack(side='left')
        
#personal frame(class)
class FormPersonal(ttk.Frame):
    def __init__(self, root, data, **kwargs):
        super().__init__(root,**kwargs)
        # country
        self.ct_label = tk.Label(self, text='country')
        self.ct_label.pack()
        countries = ['USA', 'Taiwan', 'China', 'Japan', 'British', 'Australia', 'Canada', 'South Korea']
        self.ct = ttk.Combobox(self, values=countries, textvariable=data['ct'])
        self.ct.pack()
        
        #gender
        self.gen_label = tk.Label(self, text='gender')
        self.gen_label.pack()
        self.gen = FormGender(self, data)
        self.gen.pack()
        
        #height, weight
        self.hei_label = tk.Label(self, text='height')
        self.hei_label.pack()
        self.hei = ttk.Spinbox(self, from_=90, to=200, increment=5, textvariable=data['hei'])
        self.hei.pack()
        self.wei_label = tk.Label(self, text='weight')
        self.wei_label.pack()
        self.wei = ttk.Spinbox(self, from_=20, to=90, increment=0.5, textvariable=data['wei'])
        self.wei.pack()
        
        # day of birth
        self.bd_label = tk.Label(self, text='DOB')
        self.bd_label.pack()
        self.bd_selector = Calendar(self, selectmode='day',
                                    date_pattern='mm/dd/yyyy',
                                    textvariable=data['bd'])
        self.bd_selector.pack()
        
        # 通知勾選欄位
        self.notify = ttk.Checkbutton(self, text='receiving notification', variable=data['not'])
        self.notify.pack()
        
# export and import UI(class)
class FileUI(ttk.Frame):
    def __init__(self,root,**kwargs):
        super().__init__(root,**kwargs)
        self.columnconfigure(0, weight=1, uniform='c')
        self.columnconfigure(1, weight=1, uniform='c')
        self.rowconfigure(0, weight=1, uniform='r')
        self.exp_btn = tk.Button(self, text='export', command=root.export_data)
        self.exp_btn.grid(row=0, column=0, sticky='NEWS')
        self.imp_btn = tk.Button(self, text='import', command=root.import_data)
        self.imp_btn.grid(row=0, column=1, sticky='NEWS')
    
    
# main window
class FormApp(tk.Tk):
    
    # default data
    def create_data(self):
        
        #the default form data, declaire them as "dynamica variable" by "tk.StringVariable"
        self.data = {}
        self.data['mail'] = tk.StringVar(value='wei@itt.com')
        self.data['id'] = tk.StringVar(value='wei1993')
        self.data['pw'] = tk.StringVar(value='12345678')
        self.data['ct'] = tk.StringVar(value='USA')
        self.data['gen'] = tk.StringVar(value='f')
        self.data['bd'] = tk.StringVar(value='04/05/1993')
        self.data['hei'] = tk.IntVar(value=175)
        self.data['wei'] = tk.DoubleVar(value=70.5)
        self.data['not'] = tk.BooleanVar(value=False)
    
    # export/import : convert from StringVar to Python Dict, and then convert Dict to JSON file, and vise-versa
    def export_data(self):
        out = {}
        # convert from StringVar to Python Dict
        for k, v in self.data.items():
            out[k] = v.get()           #get method is belonged to tkinter library
        
        # dump method for converting from Python Dict to json file
        with open(FILE_PATH, 'w') as file:
            json.dump(out, file)
            
    
    def import_data(self):
        # read from json, and then convert it to Python Dict
        with open(FILE_PATH, 'r') as file:
            d = json.load(file)
        
        # python Dict strings to tk StringVar
        for k, v in self.data.items():
            self.data[k].set(d[k])
    
    '''
    # modify when import
    def on_button_clicked(self):
        tmp = self.export_data()
        print(tmp)
        tmp['wei'] -= 2
        tmp['hei'] -= 5
        tmp['not'] = not(tmp['not'])
        self.import_data(tmp)
    '''
    
    def __init__(self):
        super().__init__()
        
        #create a default data
        self.create_data()
        
        # label creating
        self.title_label = ttk.Label(self, text='Welcome',  
                              background='#9F5F5F',
                              font=('Ariel', 28),
                              relief='groove')
        self.title_label.pack()
        
        # create login, personal, and fileui frames(class objects) 
        self.login = FormLogin(self, data=self.data, relief='groove')  #self.data is when enter texts into login entry
        self.login.pack(padx=10,pady=10,ipadx=10,ipady=10)
        
        self.per_label = ttk.Label(self, text='Personal Info',
                                   relief='groove')
        self.per_label.pack()
        
        self.personal = FormPersonal(self, data=self.data, relief='groove')
        self.personal.pack(padx=10,pady=10,ipadx=10,ipady=10)
        
        self.file_ui = FileUI(self, relief='groove')
        self.file_ui.pack(fill='both', padx=10,pady=10,ipadx=10,ipady=10)
        
        #self.tmp = tk.Button(self,text='testing purpose', command=self.on_button_clicked)
        #self.tmp.pack()
        
        
app = FormApp()
app.title('abc')
app.mainloop()
