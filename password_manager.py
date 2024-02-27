from tkinter import CENTER, Tk, Label, Button, Entry ,Frame ,END, Toplevel
from tkinter import ttk
from db_operations import Dboperations


class root_window:

    def __init__(self, root, db):
        self.db= db
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("900x550+40+40")

        head_title = Label(self.root, text="Password Manager", width=40,bg="green",font=("Ariel", 20), padx=10, pady=10, justify=CENTER,
                           anchor="center").grid(columnspan=4,padx=130, pady=20)
        
        self.crud_frame = Frame(self.root,highlightbackground="darkblue",highlightthickness=2, padx=10, pady=30)
        self.crud_frame.grid()
        self.create_entry_labels()
        self.create_entry_boxes()
        self.create_crud_buttons()
        self.search_entry =Entry(self.crud_frame,width=30 ,font=("Ariel",12))
        self.search_entry.grid(row=self.row_no, column=self.col_no,)
        self.col_no+=1
        Button(self.crud_frame,text="Search",bg="yellow", font=("Ariel",12), width=20).grid(row=self.row_no ,column=self.col_no, padx=5,pady=5)
        self.create_records_tree()


    def create_entry_labels(self):
        self.col_no, self.row_no =0, 0
        labels_info= ('ID','Website','Username','Password')
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg='grey',fg="white", font=("Ariel",12),padx=5,pady=2).grid(row=self.row_no, column=self.col_no,padx=5,pady=2)
            self.col_no+=1
    
    def create_crud_buttons(self):
        self.row_no+=1
        self.col_no =0
        buttons_info = (('save','green', self.save_record),('Update','blue', self.update_record),('Delete','red', self.delete_record),('copy Password','violet', self.capy_password),('Show All Records','purple',self.show_records))
        for btn_info in buttons_info:
            if btn_info[0]=='Show All Records':
                self.row_no+=1
                self.col_no=0
            Button(self.crud_frame, text=btn_info[0], bg=btn_info[1],fg="white", font=("Ariel",12),padx=2,pady=1, width=20, command=btn_info[2]).grid(row=self.row_no, column=self.col_no,padx=5,pady=10)
            self.col_no+=1



    def create_entry_boxes(self):
        self.row_no+=1
        self.enter_boxes =[]
        self.col_no=0
        for i in range(4):
            show=""
            if i==3:
                show="*"
            enter_box=Entry(self.crud_frame,width=20,background="lightgrey",font=("Ariel",12), show=show)
            enter_box.grid(row=self.row_no,column=self.col_no, padx=5, pady=2)
            self.col_no+=1
            self.enter_boxes.append(enter_box)

    def save_record(self):
        website = self.enter_boxes[1].get()
        username = self.enter_boxes[2].get()
        password = self.enter_boxes[3].get()

        data = {'website': website, 'username': username, 'password': password}
        self.db.create_record(data)
        self.show_records()

    def update_record(self):
        ID=self.enter_boxes[0].get()
        website = self.enter_boxes[1].get()
        username = self.enter_boxes[2].get()
        password = self.enter_boxes[3].get()

        data = {'ID':ID ,'website': website, 'username': username, 'password': password}
        self.db.update_record(data)
        self.show_records()


    def delete_record(self):
        ID=self.enter_boxes[0].get()
        self.db.delete_record(ID)
        self.show_records()


    def show_records(self):
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
        records_list = self.db.show_records()
        for record in records_list:
            self.records_tree.insert('', END ,values=(record[0],record[3],record[4],record[5]))


    def create_records_tree(self):
        columns=('ID', 'Website', 'username', 'password')
        self.records_tree=  ttk.Treeview(self.root ,columns=columns, show='headings')
        self.records_tree.heading('ID',text="ID")  
        self.records_tree.heading('Website',text="Website Name") 
        self.records_tree.heading('username',text="username") 
        self.records_tree.heading('password',text="password") 
        self.records_tree['displaycolumns'] = ( 'Website', 'username')


        def item_selected(event):
            for selected_item in self.records_tree.selection():
                item =self.records_tree.item(selected_item)
                record = item['values']
                for entry_box, item in zip(self.enter_boxes,record):
                    entry_box.delete(0,END)
                    entry_box.insert(0,item)

        self.records_tree.bind('<<TreeviewSelect>>',item_selected)            
        self.records_tree.grid()  

    def capy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.enter_boxes[3].get())
        message = "password Copied"
        title = "copy"
        if self.entry_boxes[3].get()=="":
            message="Box is Empty"
            title="Error"

        self.shoemessage(title,message)

    def showmessage(self, title_box:str=None,message:str=None):
        TIME_TO_WAIT =900
        root = Toplevel(self.root)
        background='green'
        if title_box == "error":
            background="red"

        root.geometry('200x30+600+200')
        root.title(title_box)
        Label(root,text=message, background=background,font=("Ariel",15),fg='white').pack(padx=4,pady=2)
        try:
            root.after(TIME_TO_WAIT, root.destroy)
        except Exception as e:
            print("error occured",e)

    



        

if __name__=="__main__" :


    db_class = Dboperations()
    db_class.create_table()
    root = Tk()
    root_class= root_window(root,db_class)
    root.mainloop()
    