from gc import disable
from pdb import pm
from tarfile import data_filter
import tkinter as tk
from tkinter import NONE, Checkbutton, ttk, messagebox, filedialog
from turtle import width
import requests
import concurrent.futures
from datetime import datetime, timedelta
import threading
import os
import time  # Add this import statement
from tkcalendar import DateEntry
import schedule
from tkinter import Radiobutton
from tkinter import messagebox
from babel import numbers
import sys

#Store Scheduled Throw of Tagss
scheduled_tag_jobs = {}

# Function to convert date string to epoch time
def date_to_epoch(date_str):
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    epoch_time = int(dt.timestamp())
    return epoch_time

#Function to Edit selected data in Table 
def edit_table():

    selected_item = data_tree.focus()
    if selected_item:
        item = data_tree.item(selected_item)['values']
        status = item[12]
        pattern = item[14]

        if str(status) == "Stop":
            messagebox.showerror("Error", "Can't be updated as this Schedule has been STOPPED.")
        elif pattern == "Immediately Run":
            messagebox.showerror("Error", "Unable to Update. This is not a Scheduled Tag.")
        else:
                
            edit_dialog = tk.Toplevel(root)
            edit_dialog.title("Edit Dialog")

            # Page ID
            edit_page_id_label = ttk.Label(edit_dialog, text="Page ID:")
            edit_page_id_label.grid(row=0, column=0, sticky=tk.W)
            edit_page_id_entry = ttk.Entry(edit_dialog)
            edit_page_id_entry.grid(row=0, column=1, sticky=tk.W)

            # Access Token
            edit_access_token_label = ttk.Label(edit_dialog, text="Access Token:")
            edit_access_token_label.grid(row=1, column=0, sticky=tk.W)
            edit_access_token_entry = ttk.Entry(edit_dialog)
            edit_access_token_entry.grid(row=1, column=1, sticky=tk.W)

            #Number of Iteration
            edit_num_iterations_label = ttk.Label(edit_dialog, text="Number of Iterations:")
            edit_num_iterations_label.grid(row=2, column=0, sticky=tk.W)
            edit_num_iterations_entry = ttk.Entry(edit_dialog)
            edit_num_iterations_entry.grid(row=2, column=1, sticky=tk.W)

            # Maximum Workers
            edit_max_workers_label = ttk.Label(edit_dialog, text="Maximum Workers:")
            edit_max_workers_label.grid(row=3, column=0, sticky=tk.W)
            edit_max_workers_entry = ttk.Entry(edit_dialog)
            edit_max_workers_entry.grid(row=3, column=1, sticky=tk.W)

            # Tag ID Name
            edit_tag_id_to_add_label = ttk.Label(edit_dialog, text="Tag Id Name:")
            edit_tag_id_to_add_label.grid(row=4, column=0, sticky=tk.W)
            edit_tag_id_to_add_entry = ttk.Entry(edit_dialog)
            edit_tag_id_to_add_entry.grid(row=4, column=1, sticky=tk.W)
            
            # Function to edit toggle the state of Shifts
            def edit_toggle_shift():
                if edit_shift_var.get() == 1:
                    edit_first_ff_checkbox.config(text="1st Throw (3 days ago)", state="normal")
                    edit_second_ff_checkbox.config(text="2nd Throw(10 days ago)", state="normal")
                    edit_third_ff_checkbox.config(text="3rd Throw(30 days ago)", state="normal")
                    edit_custom_ff_checkbox.config(state="normal")
                else:
                    edit_first_ff_checkbox.config(text="1st Throw (today @ 5PM)", state="normal")
                    edit_second_ff_checkbox.config(text="2nd Throw (today @ 8PM)", state="normal")
                    edit_third_ff_checkbox.config(text="3rd Throw (today @ 12MN/AM)", state="normal")
                    edit_custom_ff_checkbox.config(state="normal")

            def edit_toggle_batch_throw():
                if edit_first_ff_var.get() == 1 or edit_second_ff_var.get() == 1 or edit_third_ff_var.get() == 1:
                    edit_custom_ff_var.set(0)
                    edit_input_start_date_entry.config(state="disabled")
                    edit_input_end_date_entry.config(state="disabled")
                    edit_input_start_hour_combobox.config(state="disabled")
                    edit_input_start_minute_combobox.config(state="disabled")
                    edit_input_start_second_combobox.config(state="disabled")
                    edit_input_end_hour_combobox.config(state="disabled")
                    edit_input_end_minute_combobox.config(state="disabled")
                    edit_input_end_second_combobox.config(state="disabled")
                    
                    edit_input_start_date_label.grid_forget()
                    edit_input_end_date_label.grid_forget()
                    edit_input_end_date_entry.grid_forget()
                    edit_input_start_date_entry.grid_forget()
                    edit_end_time_frame.grid_forget()
                    edit_time_frame.grid_forget()
                    edit_input_start_time_label.grid_forget()
                    edit_input_end_time_label.grid_forget()


                    if edit_third_ff_var.get() == 1 and edit_second_ff_var.get() == 1 and edit_first_ff_var.get() == 1:
                        edit_on_batch1 = 1
                        edit_on_batch2 = 1
                        edit_on_batch3 = 1

                        if edit_shift_var.get() == 0:
                            edit_first_sched1.grid(row=0, column=1, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                            edit_input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                            edit_input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                            edit_first_sched.grid(row=0, column=4, sticky=tk.W)
                            edit_second_sched.grid(row=1, column=4, sticky=tk.W)
                            edit_second_sched1.grid(row=1, column=1, sticky=tk.W)
                            edit_third_sched1.grid(row=2, column=1, sticky=tk.W) 

                            edit_input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                            edit_third_sched.grid(row=2, column=4, sticky=tk.W)
                            edit_input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
                        else:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()

                    elif edit_third_ff_var.get() == 0 and edit_second_ff_var.get() == 1 and edit_first_ff_var.get() == 1:
                        edit_on_batch1 = 1
                        edit_on_batch2 = 1
                        edit_on_batch3 = 0

                        if edit_shift_var.get() == 0:
                            edit_first_sched1.grid(row=0, column=1, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                            edit_input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                            edit_input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                            edit_second_sched.grid(row=1, column=4, sticky=tk.W)
                            edit_second_sched1.grid(row=1, column=1, sticky=tk.W)
                            edit_first_sched.grid(row=0, column=4, sticky=tk.W)

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()
                        else:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            edit_third_sched1.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()

                    elif edit_third_ff_var.get() == 1 and edit_second_ff_var.get() == 0 and edit_first_ff_var.get() == 1:
                        edit_on_batch1 = 1
                        edit_on_batch2 = 0
                        edit_on_batch3 = 1

                        if edit_shift_var.get() == 0:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)
                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid(row=0, column=4, sticky=tk.W)
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            
                            edit_third_sched1.grid(row=2, column=1, sticky=tk.W) 
                            edit_input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                            edit_third_sched.grid(row=2, column=4, sticky=tk.W)
                            edit_input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
                        else:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            edit_third_sched1.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()

                    elif edit_third_ff_var.get() == 1 and edit_second_ff_var.get() == 1 and edit_first_ff_var.get() == 0:
                        edit_on_batch1 = 0
                        edit_on_batch2 = 1
                        edit_on_batch3 = 1

                        if edit_shift_var.get() == 0:
                            edit_first_sched.grid_forget()
                            edit_first_sched1.grid_forget()
                            edit_input_schedule_hour_combobox.grid_forget()
                            edit_input_schedule_minute_combobox.grid_forget()
                            edit_input_schedule_ampm_combobox.grid_forget()

                            edit_input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                            edit_input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                            edit_input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                            edit_second_sched.grid(row=1, column=4, sticky=tk.W)
                            edit_second_sched1.grid(row=1, column=1, sticky=tk.W)

                            edit_third_sched1.grid(row=2, column=1, sticky=tk.W) 
                            edit_input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                            edit_third_sched.grid(row=2, column=4, sticky=tk.W)
                            edit_input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
                        else:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            edit_third_sched1.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()

                    elif edit_third_ff_var.get() == 0 and edit_second_ff_var.get() == 0 and edit_first_ff_var.get() == 1:
                        edit_on_batch1 = 1
                        edit_on_batch2 = 0
                        edit_on_batch3 = 0

                        if edit_shift_var.get() == 0:
                            edit_first_sched.grid_forget()
                            edit_first_sched1.grid(row=0, column=1, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()

                            edit_third_sched1.grid_forget()
                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()
                        else:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            edit_third_sched1.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()

                    elif edit_third_ff_var.get() == 1 and edit_second_ff_var.get() == 0 and edit_first_ff_var.get() == 0:
                        edit_on_batch1 = 0
                        edit_on_batch2 = 0
                        edit_on_batch3 = 1
                        
                        if edit_shift_var.get() == 0:
                            edit_first_sched1.grid_forget()
                            edit_input_schedule_hour_combobox.grid_forget()
                            edit_input_schedule_minute_combobox.grid_forget()
                            edit_input_schedule_ampm_combobox.grid_forget()
                            edit_first_sched.grid_forget()

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()

                            edit_third_sched1.grid(row=2, column=1, sticky=tk.W) 
                            edit_input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                            edit_third_sched.grid(row=2, column=4, sticky=tk.W)
                            edit_input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
                        else:
                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            edit_third_sched1.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()

                    elif edit_third_ff_var.get() == 0 and edit_second_ff_var.get() == 1 and edit_first_ff_var.get() == 0:
                        edit_on_batch1 = 0
                        edit_on_batch2 = 1
                        edit_on_batch3 = 0

                        if edit_shift_var.get() == 0:
                            edit_first_sched1.grid_forget()
                            edit_input_schedule_hour_combobox.grid_forget()
                            edit_input_schedule_minute_combobox.grid_forget()
                            edit_input_schedule_ampm_combobox.grid_forget()
                            edit_first_sched.grid_forget()

                            edit_input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                            edit_input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                            edit_input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                            edit_second_sched.grid(row=1, column=4, sticky=tk.W)
                            edit_second_sched1.grid(row=1, column=1, sticky=tk.W)

                            edit_third_sched1.grid_forget()
                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()
                        else:

                            edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                            edit_input_schedule_hour_combobox2.grid_forget()
                            edit_input_schedule_minute_combobox2.grid_forget()
                            edit_input_schedule_ampm_combobox2.grid_forget()
                            edit_first_sched.grid_forget()
                            edit_second_sched.grid_forget()
                            edit_second_sched1.grid_forget()
                            edit_third_sched1.grid_forget()

                            edit_input_schedule_hour_combobox3.grid_forget()
                            edit_third_sched.grid_forget()
                            edit_input_schedule_minute_combobox3.grid_forget()
                            edit_input_schedule_ampm_combobox3.grid_forget()
                    else:
                        edit_first_sched1.grid(row=0, column=4, sticky=tk.W)
                        edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                        edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                        edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                        edit_input_schedule_hour_combobox2.grid_forget()
                        edit_input_schedule_minute_combobox2.grid_forget()
                        edit_input_schedule_ampm_combobox2.grid_forget()
                        edit_first_sched.grid_forget()
                        edit_second_sched.grid_forget()
                        edit_second_sched1.grid_forget()
                        edit_third_sched1.grid_forget()

                        edit_input_schedule_hour_combobox3.grid_forget()
                        edit_third_sched.grid_forget()
                        edit_input_schedule_minute_combobox3.grid_forget()
                        edit_input_schedule_ampm_combobox3.grid_forget()


                    if edit_third_ff_var.get() == 1:
                        # first_ff_var.set(1)
                        # second_ff_var.set(1)

                        #Check Shift
                        if edit_shift_var.get() == 1:
                            #Get Date from remaining days of this month up to yesterday (AM)
                            edit_start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                            edit_end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                            edit_start_hour = "00"
                            edit_start_minute = "00"
                            edit_start_seconds = "00"
                            edit_end_hour = "23"
                            edit_end_minute = "59"
                            edit_end_seconds = "59"
                            
                            edit_shift = 1
                            edit_batch_throw = 3
                            
                            edit_changed_schedule_hour = edit_input_schedule_hour_combobox.get()
                            edit_changed_schedule_minute = edit_input_schedule_minute_combobox.get()
                            edit_changed_schedule_ampm = edit_input_schedule_ampm_combobox.get()
                            edit_changed_schedule_hour2 = edit_input_schedule_hour_combobox2.get()
                            edit_changed_schedule_minute2 = edit_input_schedule_minute_combobox2.get()
                            edit_changed_schedule_ampm2 = edit_input_schedule_ampm_combobox2.get()
                            edit_changed_schedule_hour3 = edit_input_schedule_hour_combobox3.get()
                            edit_changed_schedule_minute3 = edit_input_schedule_minute_combobox3.get()
                            edit_changed_schedule_ampm3 = edit_input_schedule_ampm_combobox3.get()
                            
                            return edit_start_date, edit_end_date , edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3
                        else:
                            #Get(PM)
                            edit_start_date = datetime.now().strftime("%Y-%m-%d")
                            edit_end_date = datetime.now().strftime("%Y-%m-%d")
                            edit_start_hour = "00"
                            edit_start_minute = "00"
                            edit_start_seconds = "00"
                            edit_end_hour = "23"
                            edit_end_minute = "59"
                            edit_end_seconds = "59"
                            
                            edit_changed_schedule_hour = edit_input_schedule_hour_combobox.get()
                            edit_changed_schedule_minute = edit_input_schedule_minute_combobox.get()
                            edit_changed_schedule_ampm = edit_input_schedule_ampm_combobox.get()
                            edit_changed_schedule_hour2 = edit_input_schedule_hour_combobox2.get()
                            edit_changed_schedule_minute2 = edit_input_schedule_minute_combobox2.get()
                            edit_changed_schedule_ampm2 = edit_input_schedule_ampm_combobox2.get()
                            edit_changed_schedule_hour3 = edit_input_schedule_hour_combobox3.get()
                            edit_changed_schedule_minute3 = edit_input_schedule_minute_combobox3.get()
                            edit_changed_schedule_ampm3 = edit_input_schedule_ampm_combobox3.get()
                        
                            edit_input_schedule_hour_var3.set("12")
                            edit_input_schedule_minute_var3.set("00")
                            edit_input_schedule_ampm_var3.set("AM")
                            
                            edit_shift = 0
                            edit_batch_throw = 3
                    
                            return edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3
                    
                    elif edit_second_ff_var.get()==1:
                        # first_ff_var.set(1)
                        # third_ff_var.set(0)
                        #Check Shift
                        edit_on_batch2 = 1

                        if edit_shift_var.get() == 1:
                            #Get Date from 10 days ago up to yesterday (AM)
                            edit_start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
                            edit_end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                            edit_start_hour = "00"
                            edit_start_minute = "00"
                            edit_start_seconds = "00"
                            edit_end_hour = "23"
                            edit_end_minute = "59"
                            edit_end_seconds = "59"
                            
                            edit_shift = 1
                            edit_batch_throw = 2
                            
                            edit_changed_schedule_hour = edit_input_schedule_hour_combobox.get()
                            edit_changed_schedule_minute = edit_input_schedule_minute_combobox.get()
                            edit_changed_schedule_ampm = edit_input_schedule_ampm_combobox.get()
                            edit_changed_schedule_hour2 = edit_input_schedule_hour_combobox2.get()
                            edit_changed_schedule_minute2 = edit_input_schedule_minute_combobox2.get()
                            edit_changed_schedule_ampm2 = edit_input_schedule_ampm_combobox2.get()
                            edit_changed_schedule_hour3 = edit_input_schedule_hour_combobox3.get()
                            edit_changed_schedule_minute3 = edit_input_schedule_minute_combobox3.get()
                            edit_changed_schedule_ampm3 = edit_input_schedule_ampm_combobox3.get()
                            
                            return edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3
                        else:
                            #Get Date from 10 days ago up to today (PM)
                            edit_start_date = datetime.now().strftime("%Y-%m-%d")
                            edit_end_date = datetime.now().strftime("%Y-%m-%d")
                            edit_start_hour = "00"
                            edit_start_minute = "00"
                            edit_start_seconds = "00"
                            edit_end_hour = "23"
                            edit_end_minute = "59"
                            edit_end_seconds = "59"
                            
                            edit_changed_schedule_hour = edit_input_schedule_hour_combobox.get()
                            edit_changed_schedule_minute = edit_input_schedule_minute_combobox.get()
                            edit_changed_schedule_ampm = edit_input_schedule_ampm_combobox.get()
                            edit_changed_schedule_hour2 = edit_input_schedule_hour_combobox2.get()
                            edit_changed_schedule_minute2 = edit_input_schedule_minute_combobox2.get()
                            edit_changed_schedule_ampm2 = edit_input_schedule_ampm_combobox2.get()
                            edit_changed_schedule_hour3 = edit_input_schedule_hour_combobox3.get()
                            edit_changed_schedule_minute3 = edit_input_schedule_minute_combobox3.get()
                            edit_changed_schedule_ampm3 = edit_input_schedule_ampm_combobox3.get()
                            
                            edit_input_schedule_hour_var2.set("08")
                            edit_input_schedule_minute_var2.set("00")
                            edit_input_schedule_ampm_var2.set("PM")
                            
                            edit_shift = 0
                            edit_batch_throw = 2
                            
                            return edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3

                    elif edit_first_ff_var.get()==1:
                        # second_ff_var.set(0)
                        # third_ff_var.set(0)
                        
                        if edit_shift_var.get() == 1:
                            # Get the date from three days ago up to yesterday(AM)
                            edit_start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
                            edit_end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                            edit_start_hour = "00"
                            edit_start_minute = "00"
                            edit_start_seconds = "00"
                            edit_end_hour = "23"
                            edit_end_minute = "59"
                            edit_end_seconds = "59"
                            
                            edit_shift = 1
                            edit_batch_throw = 1
                            
                            edit_changed_schedule_hour = input_schedule_hour_combobox.get()
                            edit_changed_schedule_minute = input_schedule_minute_combobox.get()
                            edit_changed_schedule_ampm = input_schedule_ampm_combobox.get()
                            edit_changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                            edit_changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                            edit_changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                            edit_changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                            edit_changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                            edit_changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
                
                            return edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3
                        else:
                            # Get the date from three days ago up to today(PM)
                            edit_start_date = datetime.now().strftime("%Y-%m-%d")
                            edit_end_date = datetime.now().strftime("%Y-%m-%d")
                            edit_start_hour = "00"
                            edit_start_minute = "00"
                            edit_start_seconds = "00"
                            edit_end_hour = "23"
                            edit_end_minute = "59"
                            edit_end_seconds = "59"
                            
                            edit_changed_schedule_hour = edit_input_schedule_hour_combobox.get()
                            edit_changed_schedule_minute = edit_input_schedule_minute_combobox.get()
                            edit_changed_schedule_ampm = edit_input_schedule_ampm_combobox.get()
                            edit_changed_schedule_hour2 = edit_input_schedule_hour_combobox2.get()
                            edit_changed_schedule_minute2 = edit_input_schedule_minute_combobox2.get()
                            edit_changed_schedule_ampm2 = edit_input_schedule_ampm_combobox2.get()
                            edit_changed_schedule_hour3 = edit_input_schedule_hour_combobox3.get()
                            edit_changed_schedule_minute3 = edit_input_schedule_minute_combobox3.get()
                            edit_changed_schedule_ampm3 = edit_input_schedule_ampm_combobox3.get()
                            
                            edit_input_schedule_hour_var.set("05")
                            edit_input_schedule_minute_var.set("00")
                            edit_input_schedule_ampm_var.set("PM")
                            
                            edit_shift = 0
                            edit_batch_throw = 1
                
                            return edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3
                        
                elif edit_custom_ff_var.get() == 1:
                    edit_on_batch1 = 0
                    edit_on_batch2 = 0
                    edit_on_batch3 = 0

                    edit_input_start_date_label.grid(row=8, column=1, sticky=tk.W)
                    edit_input_end_date_label.grid(row=9, column=1, sticky=tk.W)
                    edit_input_end_date_entry.grid(row=9, column=2, sticky=tk.W)
                    edit_input_start_date_entry.grid(row=8, column=2, sticky=tk.W)
                    edit_end_time_frame.grid(row=11, column=2, columnspan=6, sticky=tk.W, pady=4)
                    edit_time_frame.grid(row=10, column=2, columnspan=6, sticky=tk.W, pady=4)
                    edit_input_start_time_label.grid(row=10, column=1, sticky=tk.W)
                    edit_input_end_time_label.grid(row=11, column=1, sticky=tk.W)

                    edit_first_ff_var.set(0)
                    edit_second_ff_var.set(0)
                    edit_third_ff_var.set(0)
                    edit_input_start_date_entry.config(state="normal")
                    edit_input_end_date_entry.config(state="normal")
                    edit_input_start_hour_combobox.config(state="normal")
                    edit_input_start_minute_combobox.config(state="normal")
                    edit_input_start_second_combobox.config(state="normal")
                    edit_input_end_hour_combobox.config(state="normal")
                    edit_input_end_minute_combobox.config(state="normal")
                    edit_input_end_second_combobox.config(state="normal")
                    
                    edit_start_date = edit_input_start_date_entry.get()
                    edit_end_date = edit_input_end_date_entry.get()
              
                    edit_start_hour = edit_input_start_hour_combobox.get()
                    edit_start_minute = edit_input_start_minute_combobox.get()
                    edit_start_seconds = edit_input_start_second_combobox.get()
                    edit_end_hour = edit_input_end_hour_combobox.get()
                    edit_end_minute = edit_input_end_minute_combobox.get()
                    edit_end_seconds = edit_input_end_second_combobox.get()

                    edit_changed_schedule_hour = edit_input_schedule_hour_combobox.get()
                    edit_changed_schedule_minute = edit_input_schedule_minute_combobox.get()
                    edit_changed_schedule_ampm = edit_input_schedule_ampm_combobox.get()
                    edit_changed_schedule_hour2 = edit_input_schedule_hour_combobox2.get()
                    edit_changed_schedule_minute2 = edit_input_schedule_minute_combobox2.get()
                    edit_changed_schedule_ampm2 = edit_input_schedule_ampm_combobox2.get()
                    edit_changed_schedule_hour3 = edit_input_schedule_hour_combobox3.get()
                    edit_changed_schedule_minute3 = edit_input_schedule_minute_combobox3.get()
                    edit_changed_schedule_ampm3 = edit_input_schedule_ampm_combobox3.get()
                    
                    edit_shift = 2
                    edit_batch_throw = 0
                    
                    return edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3
                
                elif edit_custom_ff_var.get() == 0:
                    edit_input_start_date_entry.config(state="disabled")
                    edit_input_end_date_entry.config(state="disabled")
                    edit_input_start_hour_combobox.config(state="disabled")
                    edit_input_start_minute_combobox.config(state="disabled")
                    edit_input_start_second_combobox.config(state="disabled")
                    edit_input_end_hour_combobox.config(state="disabled")
                    edit_input_end_minute_combobox.config(state="disabled")
                    edit_input_end_second_combobox.config(state="disabled")
                    
                    edit_input_start_date_label.grid_forget()
                    edit_input_end_date_label.grid_forget()
                    edit_input_end_date_entry.grid_forget()
                    edit_input_start_date_entry.grid_forget()
                    edit_end_time_frame.grid_forget()
                    edit_time_frame.grid_forget()
                    edit_input_start_time_label.grid_forget()
                    edit_input_end_time_label.grid_forget()

            #Shift Tag
            #AM Shift Radio Button Tag
            edit_shift_label = ttk.Label(edit_dialog, text="Shift:")
            edit_shift_label.grid(row=5, column=0, sticky=tk.W) 
            edit_shift_var = tk.IntVar()
            edit_am_shift_radiobutton = Radiobutton(edit_dialog, text="AM Shift", variable=edit_shift_var, value=1, command=edit_toggle_shift)
            edit_am_shift_radiobutton.grid(row=5, column=1, sticky=tk.W, pady=10)

            #PM Shift Radio Button Tag
            edit_pm_shift_radiobutton = Radiobutton(edit_dialog, text="PM Shift", variable=edit_shift_var, value=0, command=edit_toggle_shift)
            edit_pm_shift_radiobutton.grid(row=5, column=2, sticky=tk.W, pady=10)

            # Set default radio button selection
            edit_shift_var.set(1)

            #Batch Throw
            #1ST FF Throw 3 days Ago(AM) & Today @5 PM (PM)
            edit_first_ff_var = tk.IntVar()
            edit_first_ff_checkbox = Checkbutton(edit_dialog, text ="1st Throw (3 days ago)", variable=edit_first_ff_var , onvalue=1, offvalue=0, command=edit_toggle_batch_throw)
            edit_first_ff_checkbox.grid(row=6, column=1, sticky=tk.W)

            #2ND FF Throw 10 days Ago(AM) & Today @8 PM (PM)
            edit_second_ff_var = tk.IntVar()
            edit_second_ff_checkbox = Checkbutton(edit_dialog, text ="2nd Throw (10 days ago)", variable=edit_second_ff_var , onvalue=1, offvalue=0, command=edit_toggle_batch_throw)
            edit_second_ff_checkbox.grid(row=6, column=2, sticky=tk.W)

            #3RD FF Throw 30 days Ago(AM) & Today @12MN/AM (PM)
            edit_third_ff_var = tk.IntVar()
            edit_third_ff_checkbox = Checkbutton(edit_dialog, text ="3rd Throw (30 days ago)", variable=edit_third_ff_var , onvalue=1, offvalue=0, command=edit_toggle_batch_throw)
            edit_third_ff_checkbox.grid(row=6, column=3, sticky=tk.W)

            #Custom FF Throw
            edit_custom_ff_var = tk.IntVar()
            edit_custom_ff_checkbox = Checkbutton(edit_dialog, text ="Custom", variable=edit_custom_ff_var , onvalue=1, offvalue=0, command=edit_toggle_batch_throw)
            edit_custom_ff_checkbox.grid(row=7, column=1, sticky=tk.W)

            #Custome Date & Time Range Throw FF
            # Input Start Date
            edit_input_start_date_label = ttk.Label(edit_dialog, text="Start Date (YYYY-MM-DD):")
            edit_input_start_date_label.grid_forget()
            edit_input_start_date_entry = ttk.Entry(edit_dialog)
            edit_input_start_date_entry.grid_forget()
            edit_input_start_date_entry.config(state="disabled")


            # Input End Date
            edit_input_end_date_label = ttk.Label(edit_dialog, text="End Date (YYYY-MM-DD):")
            edit_input_end_date_label.grid_forget()
            edit_input_end_date_entry = ttk.Entry(edit_dialog)
            edit_input_end_date_entry.grid_forget()
            edit_input_end_date_entry.config(state="disabled")

            #Conversation Start Time Frame
            edit_time_frame = ttk.Frame(edit_dialog)
            edit_time_frame.grid_forget()

            # Input Start Time
            edit_input_start_time_label = ttk.Label(edit_dialog, text="Start Time:")  # Updated label text
            edit_input_start_time_label.grid_forget()

            # Start Hour Dropdown (24-hour format)
            edit_hour_options = [f"{hour:02d}" for hour in range(0, 24)]  # Hours from 0 to 23 for 24-hour format
            edit_input_start_hour_var = tk.StringVar()  # New: Variable to store selected hour
            edit_input_start_hour_combobox = ttk.Combobox(edit_time_frame, textvariable=edit_input_start_hour_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_start_hour_combobox['values'] = edit_hour_options  # New: Values for the dropdown
            edit_input_start_hour_combobox.current(0)  # New: Default selection
            edit_input_start_hour_combobox.grid(row=0, column=0, sticky=tk.W)
            edit_input_start_hour_combobox.config(state="disabled")

            # Colon Label (Start Hour and Minute separator)
            ttk.Label(edit_time_frame, text=":").grid(row=0, column=1, sticky=tk.W)  # New

            # Start Minute Dropdown
            edit_minute_options = [f"{minute:02d}" for minute in range(0, 60)]  # Minutes from 0 to 59
            edit_input_start_minute_var = tk.StringVar()  # New: Variable to store selected minute
            edit_input_start_minute_combobox = ttk.Combobox(edit_time_frame, textvariable=edit_input_start_minute_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_start_minute_combobox['values'] = edit_minute_options  # New: Values for the dropdown
            edit_input_start_minute_combobox.current(0)  # New: Default selection
            edit_input_start_minute_combobox.grid(row=0, column=2, sticky=tk.W)  # New
            edit_input_start_minute_combobox.config(state="disabled")

            # Start Colon Label (Minute and Second separator)
            ttk.Label(edit_time_frame, text=":").grid(row=0, column=3, sticky=tk.W)  # New

            # Start Second Dropdown
            edit_second_options = [f"{second:02d}" for second in range(0, 60)]  # Seconds from 0 to 59
            edit_input_start_second_var = tk.StringVar()  # New: Variable to store selected second
            edit_input_start_second_combobox = ttk.Combobox(edit_time_frame, textvariable=edit_input_start_second_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_start_second_combobox['values'] = edit_second_options  # New: Values for the dropdown
            edit_input_start_second_combobox.current(0)  # New: Default selection
            edit_input_start_second_combobox.grid(row=0, column=4, sticky=tk.W)  # New
            edit_input_start_second_combobox.config(state="disabled")

            #Conversation End Time Frame
            edit_end_time_frame = ttk.Frame(edit_dialog)
            edit_end_time_frame.grid_forget()

            # Input End Time 
            edit_input_end_time_label = ttk.Label(edit_dialog, text="End Time:")  # Updated label text
            edit_input_end_time_label.grid_forget()  # New

            # End Hour Dropdown (24-hour format)
            edit_hour_options = [f"{hour:02d}" for hour in range(0, 24)]  # Hours from 0 to 23 for 24-hour format
            edit_input_end_hour_var = tk.StringVar()  # New: Variable to store selected hour
            edit_input_end_hour_combobox = ttk.Combobox(edit_end_time_frame, textvariable=edit_input_end_hour_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_end_hour_combobox['values'] = edit_hour_options  # New: Values for the dropdown
            edit_input_end_hour_combobox.current(0)  # New: Default selection
            edit_input_end_hour_combobox.grid(row=0, column=0, sticky=tk.W)  # New
            edit_input_end_hour_combobox.config(state="disabled")

            # Colon Label (End Hour and Minute separator)
            ttk.Label(edit_end_time_frame, text=":").grid(row=0, column=1, sticky=tk.W)  # New

            # End Minute Dropdown
            edit_minute_options = [f"{minute:02d}" for minute in range(0, 60)]  # Minutes from 0 to 59
            edit_input_end_minute_var = tk.StringVar()  # New: Variable to store selected minute
            edit_input_end_minute_combobox = ttk.Combobox(edit_end_time_frame, textvariable=edit_input_end_minute_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_end_minute_combobox['values'] = edit_minute_options  # New: Values for the dropdown
            edit_input_end_minute_combobox.current(0)  # New: Default selection
            edit_input_end_minute_combobox.grid(row=0, column=2, sticky=tk.W)  # New
            edit_input_end_minute_combobox.config(state="disabled")

            # End Colon Label (Minute and Second separator)
            ttk.Label(edit_end_time_frame, text=":").grid(row=0, column=3, sticky=tk.W)  # New

            # End Second Dropdown End Conversational Time
            edit_second_options = [f"{second:02d}" for second in range(0, 60)]  # Seconds from 0 to 59
            edit_input_end_second_var = tk.StringVar()  # New: Variable to store selected second
            edit_input_end_second_combobox = ttk.Combobox(edit_end_time_frame, textvariable=edit_input_end_second_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_end_second_combobox['values'] = edit_second_options  # New: Values for the dropdown
            edit_input_end_second_combobox.current(0)  # New: Default selection
            edit_input_end_second_combobox.grid(row=0, column=4, sticky=tk.W)  # New
            edit_input_end_second_combobox.config(state="disabled")

            edit_sched_date_frame = ttk.Frame(edit_dialog)
            edit_sched_date_frame.grid(row=13, column=1, columnspan=6, sticky=tk.W, pady=4)

            # Input Schedule Date  # New
            edit_input_schedule_date_label = ttk.Label(edit_dialog, text="Schedule Date:")  # New
            edit_input_schedule_date_label.grid(row=13, column=0, sticky=tk.W)  # New
            #Start Schedule Date
            edit_input_start_schedule_date_entry = DateEntry(edit_sched_date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)  # New: DateEntry widget  # New
            edit_input_start_schedule_date_entry.grid(row=0, column=0, sticky=tk.W)  # New
            ttk.Label(edit_sched_date_frame, text=" to ").grid(row=0, column=1, sticky=tk.W)
            #End Schedule Date
            edit_input_end_schedule_date_entry = DateEntry(edit_sched_date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)  # New: DateEntry widget  # New
            edit_input_end_schedule_date_entry.grid(row=0, column=2, sticky=tk.W)  # New

            #Schdule
            def edit_toggle_schedule(*args):       
                edit_selected_pattern = edit_input_schedule_pattern_combobox.get()
                print(edit_selected_pattern)
                if edit_selected_pattern == "Once":
                    edit_input_end_schedule_date_entry.set_date(edit_input_start_schedule_date_entry.get())
                    print(edit_input_start_hour_combobox.get())
                    edit_input_weekly_pattern_combobox.grid_forget()
                    edit_weekly_label.grid_forget()
                elif edit_selected_pattern == "Weekly":
                    edit_weekly_label.grid(row=0, column=6, sticky=tk.W)
                    edit_input_weekly_pattern_combobox.grid(row=0, column=7, sticky=tk.W)
                else:
                    edit_input_weekly_pattern_combobox.grid_forget()
                    edit_weekly_label.grid_forget()

            # Pattern Schedule Dropdown
            ttk.Label(edit_sched_date_frame, text=" ").grid(row=0, column=3, sticky=tk.W)
            edit_schedule_pattern_options = ["Once", "Weekly", "Everyday"]
           
            edit_input_schedule_pattern_var = tk.StringVar()  # New: Variable to store selected Schedule Pattern 
            edit_input_schedule_pattern_var.trace("w", edit_toggle_schedule )
            edit_input_schedule_pattern_combobox = ttk.Combobox(edit_sched_date_frame, textvariable=edit_input_schedule_pattern_var, state="readonly", width=10)  # New: Combobox widget
            edit_input_schedule_pattern_combobox['values'] = edit_schedule_pattern_options  # New: Values for the dropdown
            edit_input_schedule_pattern_combobox.current(0)  # New: Default selection
            edit_input_schedule_pattern_combobox.grid(row=0, column=4, sticky=tk.W)  # New
            
            #Weekly Schdule Pattern
            ttk.Label(edit_sched_date_frame, text=" ").grid(row=0, column=5, sticky=tk.W)
            edit_weekly_label = ttk.Label(edit_sched_date_frame, text="Every:")
            edit_weekly_label.grid_forget()
            edit_weekly_pattern_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            edit_input_weekly_pattern_var = tk.StringVar()  # New: Variable to store selected Schedule Pattern
            edit_input_weekly_pattern_combobox = ttk.Combobox(edit_sched_date_frame, textvariable=edit_input_weekly_pattern_var, state="readonly", width=10)  # New: Combobox widget
            edit_input_weekly_pattern_combobox['values'] = edit_weekly_pattern_options  # New: Values for the dropdown
            edit_input_weekly_pattern_combobox.current(0)  # New: Default selection
            edit_input_weekly_pattern_combobox.grid_forget()  # New

            #DEFAULT WEEK
            edit_current_day_of_week = current_date.weekday()
            edit_input_weekly_pattern_combobox.current(edit_current_day_of_week)

            #Conversation Schedule Time Frame
            edit_sched_time_frame = ttk.Frame(edit_dialog)
            edit_sched_time_frame.grid(row=14, column=1, columnspan=6, sticky=tk.W, pady=4)

            # Input Schedule Time  # New
            edit_input_schedule_time_label = ttk.Label(edit_dialog, text="Schedule Time:")  # New
            edit_input_schedule_time_label.grid(row=14, column=0, sticky=tk.W)  # New

            # Hour Dropdown
            edit_hour_options = [f"{hour:02d}" for hour in range(1, 13)]  # Hours from 1 to 12
            edit_input_schedule_hour_var = tk.StringVar()  # New: Variable to store selected hour
            edit_input_schedule_hour_combobox = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_hour_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_schedule_hour_combobox['values'] = edit_hour_options  # New: Values for the dropdown
            edit_input_schedule_hour_combobox.current(0)  # New: Default selection
            edit_input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)  # New

            # Colon Label
            edit_first_sched1 = ttk.Label(edit_sched_time_frame, text=":")
            edit_first_sched1.grid(row=0, column=1, sticky=tk.W)  # New

            # Minute Dropdown
            edit_minute_options = [f"{minute:02d}" for minute in range(0, 60, 1)]  # Minutes from 0 to 55 with 5-minute intervals
            edit_input_schedule_minute_var = tk.StringVar()  # New: Variable to store selected minute
            edit_input_schedule_minute_combobox = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_minute_var, state="readonly", width=5)  # New: Combobox widget
            edit_input_schedule_minute_combobox['values'] = edit_minute_options  # New: Values for the dropdown
            edit_input_schedule_minute_combobox.current(0)  # New: Default selection
            edit_input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)  # New

            # AM/PM Dropdown
            edit_ampm_options = ["AM", "PM"]
            edit_input_schedule_ampm_var = tk.StringVar()  # New: Variable to store selected AM/PM
            edit_input_schedule_ampm_combobox = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_ampm_var, state="readonly", width=3)  # New: Combobox widget
            edit_input_schedule_ampm_combobox['values'] = edit_ampm_options  # New: Values for the dropdown
            edit_input_schedule_ampm_combobox.current(0)  # New: Default selection
            edit_input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)  # New

            edit_first_sched = ttk.Label(edit_sched_time_frame, text="1st Throw Schedule Time")
            edit_first_sched.grid_forget()

            # 2ND Throw PM Schedule
            # Hour Dropdown
            edit_hour_options2 = [f"{hour:02d}" for hour in range(1, 13)]  # Hours from 1 to 12
            edit_input_schedule_hour_var2 = tk.StringVar()  # New: Variable to store selected hour
            edit_input_schedule_hour_combobox2 = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_hour_var2, state="readonly", width=5)  # New: Combobox widget
            edit_input_schedule_hour_combobox2['values'] = edit_hour_options2  # New: Values for the dropdown
            edit_input_schedule_hour_combobox2.current(0)  # New: Default selection
            edit_input_schedule_hour_combobox2.grid_forget()  # New

            # Colon Label
            edit_second_sched1 = ttk.Label(edit_sched_time_frame, text=":")
            edit_second_sched1.grid_forget() # New

            # Minute Dropdown
            edit_minute_options2 = [f"{minute:02d}" for minute in range(0, 60, 1)]  # Minutes from 0 to 55 with 5-minute intervals
            edit_input_schedule_minute_var2 = tk.StringVar()  # New: Variable to store selected minute
            edit_input_schedule_minute_combobox2 = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_minute_var2, state="readonly", width=5)  # New: Combobox widget
            edit_input_schedule_minute_combobox2['values'] = edit_minute_options2  # New: Values for the dropdown
            edit_input_schedule_minute_combobox2.current(0)  # New: Default selection
            edit_input_schedule_minute_combobox2.grid_forget() # New

            # AM/PM Dropdown
            edit_ampm_options2 = ["AM", "PM"]
            edit_input_schedule_ampm_var2 = tk.StringVar()  # New: Variable to store selected AM/PM
            edit_input_schedule_ampm_combobox2 = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_ampm_var2, state="readonly", width=3)  # New: Combobox widget
            edit_input_schedule_ampm_combobox2['values'] = edit_ampm_options2  # New: Values for the dropdown
            edit_input_schedule_ampm_combobox2.current(0)  # New: Default selection
            edit_input_schedule_ampm_combobox2.grid_forget()  # New

            edit_second_sched = ttk.Label(edit_sched_time_frame, text="2nd Throw Schedule Time")
            edit_second_sched.grid_forget()

            # 3RD Throw PM Schedule
            # Hour Dropdown
            edit_hour_options3 = [f"{hour:02d}" for hour in range(1, 13)]  # Hours from 1 to 12
            edit_input_schedule_hour_var3 = tk.StringVar()  # New: Variable to store selected hour
            edit_input_schedule_hour_combobox3 = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_hour_var3, state="readonly", width=5)  # New: Combobox widget
            edit_input_schedule_hour_combobox3['values'] = edit_hour_options3  # New: Values for the dropdown
            edit_input_schedule_hour_combobox3.current(0)  # New: Default selection
            edit_input_schedule_hour_combobox3.grid_forget()# New

            # Colon Label
            edit_third_sched1 = ttk.Label(edit_sched_time_frame, text=":")
            edit_third_sched1.grid_forget()  # New

            # Minute Dropdown
            edit_minute_options3 = [f"{minute:02d}" for minute in range(0, 60, 1)]  # Minutes from 0 to 55 with 5-minute intervals
            edit_input_schedule_minute_var3 = tk.StringVar()  # New: Variable to store selected minute
            edit_input_schedule_minute_combobox3 = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_minute_var3, state="readonly", width=5)  # New: Combobox widget
            edit_input_schedule_minute_combobox3['values'] = edit_minute_options3  # New: Values for the dropdown
            edit_input_schedule_minute_combobox3.current(0)  # New: Default selection
            edit_input_schedule_minute_combobox3.grid_forget() # New

            # AM/PM Dropdown
            edit_ampm_options3 = ["AM", "PM"]
            edit_input_schedule_ampm_var3 = tk.StringVar()  # New: Variable to store selected AM/PM
            edit_input_schedule_ampm_combobox3 = ttk.Combobox(edit_sched_time_frame, textvariable=edit_input_schedule_ampm_var3, state="readonly", width=3)  # New: Combobox widget
            edit_input_schedule_ampm_combobox3['values'] = edit_ampm_options3  # New: Values for the dropdown
            edit_input_schedule_ampm_combobox3.current(0)  # New: Default selection
            edit_input_schedule_ampm_combobox3.grid_forget()  # New

            edit_third_sched = ttk.Label(edit_sched_time_frame, text="3rd Throw Schedule Time")
            edit_third_sched.grid_forget()

            edit_dialog.transient(root)
            edit_dialog.grab_set()

            #Close /Cancel Edit
            def close_dialog():
                edit_dialog.destroy()
                # Once the dialog is closed, release input focus
                root.focus_set()
            
            #Edit Tag 
            def edit_tag():
                selected_item = data_tree.focus()
                if selected_item:
                    item = data_tree.item(selected_item)['values']
                    selected_page_id = item[0]
                    selected_sched_start_date = item[9]  # Index of input_start_schedule_date in your data tree
                    selected_sched_time = item[10]
                    status = item[12]

                    if str(status) == "Stop":
                        edit_dialog.destroy()
                        # Once the dialog is closed, release input focus
                        root.focus_set()
                        messagebox.showerror("Error", "Can't be updated as this Schedule has been STOPPED.")
                    else:
                        # Construct the key
                        key = (str(selected_page_id), selected_sched_start_date, selected_sched_time)
                        
                        # Check if the key exists in the dictionary
                        if key in scheduled_tag_jobs:

                            #Data Set in Selected Throws
                            edit_start_date, edit_end_date, edit_start_hour, edit_start_minute, edit_start_seconds, edit_end_hour, edit_end_minute, edit_end_seconds, edit_shift, edit_batch_throw, edit_changed_schedule_hour, edit_changed_schedule_minute, edit_changed_schedule_ampm, edit_changed_schedule_hour2, edit_changed_schedule_minute2, edit_changed_schedule_ampm2, edit_changed_schedule_hour3, edit_changed_schedule_minute3, edit_changed_schedule_ampm3, edit_on_batch1, edit_on_batch2, edit_on_batch3 = edit_toggle_batch_throw()
                            
                            #GET Job to be Updated
                            scheduled_job_info = scheduled_tag_jobs[key]
                            job = scheduled_job_info["job"]

                            #Cancel the Selected Old Scheduled Tag
                            schedule.cancel_job(job)
                            del scheduled_tag_jobs[key]

                            page_id = edit_page_id_entry.get()
                            access_token = edit_access_token_entry.get()
                            num_iterations = edit_num_iterations_entry.get()
                            max_workers = edit_max_workers_entry.get()
                            tag_id_name = edit_tag_id_to_add_entry.get()
                            input_start_date = edit_input_start_date_entry.get()
                            input_end_date = edit_input_end_date_entry.get()
                            input_start_hour = edit_input_start_hour_combobox.get()
                            input_start_minute = edit_input_start_minute_combobox.get()
                            input_start_second = edit_input_start_second_combobox.get()
                            input_end_hour = edit_input_end_hour_combobox.get()
                            input_end_minute = edit_input_end_minute_combobox.get()
                            input_end_second = edit_input_end_second_combobox.get()
                            shift = edit_shift_var.get()
                            batch_throw = edit_batch_throw
                            input_start_schedule_date = edit_input_start_schedule_date_entry.get()
                            input_end_schedule_date = edit_input_end_schedule_date_entry.get()
                            scheduled_pattern = edit_input_schedule_pattern_combobox.get()
                            weekly_pattern = edit_input_weekly_pattern_combobox.get()
                            on_batch1 = edit_on_batch1
                            on_batch2 = edit_on_batch2
                            on_batch3 = edit_on_batch3

                            if shift == 0:
                                #Check if the Default Scehduled Time changed
                                if edit_on_batch1 == 1:
                                    if edit_changed_schedule_hour != "05" or edit_changed_schedule_minute != "00" or edit_changed_schedule_ampm != "PM":
                                        #Conversation Date & Time
                                        input_start_date = edit_start_date
                                        input_end_date = edit_end_date
                                        input_start_hour = edit_start_hour
                                        input_start_minute = edit_start_minute
                                        input_start_second = edit_start_seconds
                                        input_end_hour = edit_end_hour
                                        input_end_minute = edit_end_minute
                                        input_end_second = edit_end_seconds
                                        
                                        #Changed Schedule Time
                                        schedule_hour = edit_changed_schedule_hour
                                        schedule_minute = edit_changed_schedule_minute
                                        schedule_ampm = edit_changed_schedule_ampm
                                        edit_input_schedule_hour_var.set(schedule_hour)
                                        edit_input_schedule_minute_var.set(schedule_minute)
                                        edit_input_schedule_ampm_var.set(schedule_ampm)

                                        on_batch1 = 1
                                        on_batch2 = 0
                                        on_batch3 = 0

                                        display_throw = 1
                                    else:
                                        #Conversation Date & Time
                                        input_start_date = edit_start_date
                                        input_end_date = edit_end_date
                                        input_start_hour = edit_start_hour
                                        input_start_minute = edit_start_minute
                                        input_start_second = edit_start_seconds
                                        input_end_hour = edit_end_hour
                                        input_end_minute = edit_end_minute
                                        input_end_second = edit_end_seconds

                                        schedule_hour = edit_input_schedule_hour_combobox.get()
                                        schedule_minute = edit_input_schedule_minute_combobox.get()
                                        schedule_ampm = edit_input_schedule_ampm_combobox.get()

                                        on_batch1 = 1
                                        on_batch2 = 0
                                        on_batch3 = 0

                                        display_throw = 1

                                elif edit_on_batch2 == 1:
                                    if edit_changed_schedule_hour2 != "08" or edit_changed_schedule_minute2 != "00" or edit_changed_schedule_ampm2 != "PM":
                                        #Conversation Date & Time
                                        input_start_date = edit_start_date
                                        input_end_date = edit_end_date
                                        input_start_hour = edit_start_hour
                                        input_start_minute = edit_start_minute
                                        input_start_second = edit_start_seconds
                                        input_end_hour = edit_end_hour
                                        input_end_minute = edit_end_minute
                                        input_end_second = edit_end_seconds
                                        
                                        schedule_hour = edit_changed_schedule_hour2
                                        schedule_minute = edit_changed_schedule_minute2
                                        schedule_ampm = edit_changed_schedule_ampm2
                                        edit_input_schedule_hour_var2.set(schedule_hour)
                                        edit_input_schedule_minute_var2.set(schedule_minute)
                                        edit_input_schedule_ampm_var2.set(schedule_ampm)

                                        on_batch1 = 0
                                        on_batch2 = 1
                                        on_batch3 = 0

                                        display_throw = 2
                                    else:
                                        #Conversation Date & Time
                                        input_start_date = edit_start_date
                                        input_end_date = edit_end_date
                                        input_start_hour = edit_start_hour
                                        input_start_minute = edit_start_minute
                                        input_start_second = edit_start_seconds
                                        input_end_hour = edit_end_hour
                                        input_end_minute = edit_end_minute
                                        input_end_second = edit_end_seconds
                                        
                                        schedule_hour = edit_input_schedule_hour_combobox2.get()
                                        schedule_minute = edit_input_schedule_minute_combobox2.get()
                                        schedule_ampm = edit_input_schedule_ampm_combobox2.get()

                                        on_batch1 = 0
                                        on_batch2 = 1
                                        on_batch3 = 0

                                        display_throw = 2
                                
                                elif edit_on_batch3 == 1:
                                    if edit_changed_schedule_hour3 != "12" or edit_changed_schedule_minute3 != "00" or edit_changed_schedule_ampm3 != "AM":
                                        #Conversation Date & Time
                                        input_start_date = edit_start_date
                                        input_end_date = edit_end_date
                                        input_start_hour = edit_start_hour
                                        input_start_minute = edit_start_minute
                                        input_start_second = edit_start_seconds
                                        input_end_hour = edit_end_hour
                                        input_end_minute = edit_end_minute
                                        input_end_second = edit_end_seconds
                                        
                                        schedule_hour = edit_changed_schedule_hour3
                                        schedule_minute = edit_changed_schedule_minute3
                                        schedule_ampm = edit_changed_schedule_ampm3
                                        edit_input_schedule_hour_var3.set(schedule_hour)
                                        edit_input_schedule_minute_var3.set(schedule_minute)
                                        edit_input_schedule_ampm_var3.set(schedule_ampm)

                                        on_batch1 = 0
                                        on_batch2 = 0
                                        on_batch3 = 1

                                        display_throw = 3
                                    else:
                                        #Conversation Date & Time
                                        input_start_date = edit_start_date
                                        input_end_date = edit_end_date
                                        input_start_hour = edit_start_hour
                                        input_start_minute = edit_start_minute
                                        input_start_second = edit_start_seconds
                                        input_end_hour = edit_end_hour
                                        input_end_minute = edit_end_minute
                                        input_end_second = edit_end_seconds
                                        
                                        schedule_hour = edit_input_schedule_hour_combobox3.get()
                                        schedule_minute = edit_input_schedule_minute_combobox3.get()
                                        schedule_ampm = edit_input_schedule_ampm_combobox3.get()

                                        on_batch1 = 0
                                        on_batch2 = 0
                                        on_batch3 = 1

                                        display_throw = 3
                                else:
                                    schedule_hour = edit_input_schedule_hour_combobox.get()
                                    schedule_minute = edit_input_schedule_minute_combobox.get()
                                    schedule_ampm = edit_input_schedule_ampm_combobox.get()

                                    display_throw = "Custom"
                            else:
                                if on_batch1 == 1 or on_batch2 == 1 or on_batch3 == 1:
                                    input_start_date = edit_start_date
                                    input_end_date = edit_end_date
                                    input_start_hour = edit_start_hour
                                    input_start_minute = edit_start_minute
                                    input_start_second = edit_start_seconds
                                    input_end_hour = edit_end_hour
                                    input_end_minute = edit_end_minute
                                    input_end_second = edit_end_seconds

                                    if on_batch1 == 1 and on_batch2 == 0 and on_batch3 == 0:
                                        display_throw = 1
                                    elif on_batch1 == 0 and on_batch2 == 1 and on_batch3 == 0:
                                        display_throw = 2
                                    elif on_batch1 == 0 and on_batch2 == 0 and on_batch3 == 1:
                                        display_throw = 3
                                    elif on_batch1 == 1 and on_batch2 == 1 and on_batch3 == 0:
                                        display_throw = "1, 2"
                                    elif on_batch1 == 1 and on_batch2 == 0 and on_batch3 == 1:
                                        display_throw = "1, 3"
                                    elif on_batch1 == 0 and on_batch2 == 1 and on_batch3 == 1:
                                        display_throw = "2, 3"
                                    elif on_batch1 == 1 and on_batch2 == 1 and on_batch3 == 1:
                                        display_throw = "1, 2, 3"
                                    else:
                                        display_throw = "Custom"

                                else:
                                    display_throw = "Custom"

                                schedule_hour = edit_input_schedule_hour_combobox.get()
                                schedule_minute = edit_input_schedule_minute_combobox.get()
                                schedule_ampm = edit_input_schedule_ampm_combobox.get()

                            #GET Updated Data -----------------
                            if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                                scheduled_time1 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                                scheduled_datetime1 = combine_date_time(input_start_schedule_date, scheduled_time1)
                                scheduled_time2 = scheduled_datetime1.strftime("%H:%M")
                                job = schedule.every().day.at(scheduled_time2).do(execute_task, page_id, access_token, int(num_iterations), int(max_workers), tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                                # This is for Filter stop and edit Schedule
                                schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"

                                # Store entire data set associated with scheduled job
                                data_of_scheduled_tag = {
                                    "page_id": page_id,
                                    "access_token": access_token,
                                    "num_iterations": num_iterations,
                                    "max_workers": max_workers,
                                    "tag_id_name": tag_id_name,
                                    "input_start_date": input_start_date,
                                    "input_end_date": input_end_date,
                                    "input_start_hour": input_start_hour,
                                    "input_start_minute": input_start_minute,
                                    "input_start_second": input_start_second,
                                    "input_end_hour": input_end_hour,
                                    "input_end_minute": input_end_minute,
                                    "input_end_second": input_end_second,
                                    "shift": shift,
                                    "batch_throw": batch_throw,
                                    "input_start_schedule_date": input_start_schedule_date,
                                    "schedule_hour": schedule_hour,
                                    "schedule_minute": schedule_minute,
                                    "schedule_ampm": schedule_ampm,
                                    "input_end_schedule_date": input_end_schedule_date,
                                    "scheduled_pattern": scheduled_pattern,
                                    "weekly_pattern": None,
                                    "on_batch1": on_batch1,
                                    "on_batch2": on_batch2,
                                    "on_batch3": on_batch3
                                }

                                scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time4] = {
                                    "job": job,
                                    "data": data_of_scheduled_tag
                                }

                                
                            # -----------------
                            
                                # Update the status in your data tree

                                conversation_start_time = f"{input_start_hour}:{input_start_minute} {input_start_second}"
                                conversation_end_time = f"{input_end_hour}:{input_end_minute} {input_end_second}"

                                data_tree.set(selected_item, "Status", "Updated")
                                data_tree.set(selected_item, "Page ID", page_id)
                                data_tree.set(selected_item, "Access Token", access_token)
                                data_tree.set(selected_item, "Iterations", num_iterations)
                                data_tree.set(selected_item, "Max Workers", max_workers)
                                data_tree.set(selected_item, "Tag Name", tag_id_name)
                                data_tree.set(selected_item, "Start Date", input_start_date)
                                data_tree.set(selected_item, "End Date", input_end_date)
                                data_tree.set(selected_item, "Start Time", conversation_start_time)
                                data_tree.set(selected_item, "End Time", conversation_end_time)
                                display_schedule_time = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                                data_tree.set(selected_item, "Scheduled Date",input_start_schedule_date )
                                data_tree.set(selected_item, "Scheduled Time", display_schedule_time)
                                data_tree.set(selected_item, "Batch", display_throw)
                                data_tree.set(selected_item,"Schedule", scheduled_pattern)

                                # Check if the scheduled date has passed
                                
                                scheduled_datetime = combine_date_time(input_start_schedule_date, scheduled_time1)
                                if scheduled_datetime <= datetime.now():
                                    # Change the color of the scheduled text to blue
                                    data_tree.item(selected_item, tags=("blue_text",))
                
                                    # Apply the blue text tag to the scheduled date and time
                                    data_tree.tag_configure("blue_text", foreground="blue")
                                else:
                                    data_tree.item(selected_item, tags=("black_text",))
                
                                    # Apply the blue text tag to the scheduled date and time
                                    data_tree.tag_configure("black_text", foreground="black")

                                close_dialog()

                            else:
                                day_to_method = {
                                    'Monday': schedule.every().monday,
                                    'Tuesday': schedule.every().tuesday,
                                    'Wednesday': schedule.every().wednesday,
                                    'Thursday': schedule.every().thursday,
                                    'Friday': schedule.every().friday,
                                    'Saturday': schedule.every().saturday,
                                    'Sunday': schedule.every().sunday
                                }
                                            
                                week_day = weekly_pattern
                                print(week_day)
                                            
                                scheduled_time1 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                                scheduled_datetime1 = combine_date_time(input_start_schedule_date, scheduled_time1)
                                scheduled_time2 = scheduled_datetime1.strftime("%H:%M")
                                job = day_to_method[week_day].at(scheduled_time2).do(execute_task, page_id, access_token, int(num_iterations), int(max_workers), tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                                        
                                #Save data of schedule (for stop and ediy schedule)
                                schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                                data_of_scheduled_tag = schedule_time4, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3
                                scheduled_tag_jobs[data_of_scheduled_tag] = job
                                
                                schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"

                                print("anchor", schedule_time4)

                                # Store entire data set associated with scheduled job
                                data_of_scheduled_tag = {
                                    "page_id": page_id,
                                    "access_token": access_token,
                                    "num_iterations": num_iterations,
                                    "max_workers": max_workers,
                                    "tag_id_name": tag_id_name,
                                    "input_start_date": input_start_date,
                                    "input_end_date": input_end_date,
                                    "input_start_hour": input_start_hour,
                                    "input_start_minute": input_start_minute,
                                    "input_start_second": input_start_second,
                                    "input_end_hour": input_end_hour,
                                    "input_end_minute": input_end_minute,
                                    "input_end_second": input_end_second,
                                    "shift": shift,
                                    "batch_throw": batch_throw,
                                    "input_start_schedule_date": input_start_schedule_date,
                                    "schedule_hour": schedule_hour,
                                    "schedule_minute": schedule_minute,
                                    "schedule_ampm": schedule_ampm,
                                    "input_end_schedule_date": input_end_schedule_date,
                                    "scheduled_pattern": scheduled_pattern,
                                    "weekly_pattern": week_day,
                                    "on_batch1": on_batch1,
                                    "on_batch2": on_batch2,
                                    "on_batch3": on_batch3
                                }


                                scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time4] = {
                                    "job": job,
                                    "data": data_of_scheduled_tag
                                }

                                print("batch1:weekly", scheduled_tag_jobs)

                                conversation_start_time = f"{input_start_hour}:{input_start_minute} {input_start_second}"
                                conversation_end_time = f"{input_end_hour}:{input_end_minute} {input_end_second}"
                                

                                # Update the status in your data tree
                                data_tree.set(selected_item, "Status", "Updated")
                                data_tree.set(selected_item, "Page ID", page_id)
                                data_tree.set(selected_item, "Access Token", access_token)
                                data_tree.set(selected_item, "Iterations", num_iterations)
                                data_tree.set(selected_item, "Max Workers", max_workers)
                                data_tree.set(selected_item, "Tag Name", tag_id_name)
                                data_tree.set(selected_item, "Start Date", input_start_date)
                                data_tree.set(selected_item, "End Date", input_end_date)
                                data_tree.set(selected_item, "End Date", input_end_date)
                                data_tree.set(selected_item, "Start Time", conversation_start_time)
                                data_tree.set(selected_item, "End Time", conversation_end_time)

                                display_schedule_time = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                                data_tree.set(selected_item, "Scheduled Date",input_start_schedule_date )
                                data_tree.set(selected_item, "Scheduled Time", display_schedule_time)
                                data_tree.set(selected_item, "Batch", display_throw)
                                data_tree.set(selected_item, "Schedule", f"{scheduled_pattern}:{weekly_pattern}")

                                # Check if the scheduled date has passed
                                
                                scheduled_datetime = combine_date_time(input_start_schedule_date, scheduled_time1)
                                if scheduled_datetime <= datetime.now():
                                    # Change the color of the scheduled text to blue
                                    data_tree.item(selected_item, tags=("blue_text",))
                
                                    # Apply the blue text tag to the scheduled date and time
                                    data_tree.tag_configure("blue_text", foreground="blue")
                                else:
                                    # Apply the blue text tag to the scheduled date and time
                                    data_tree.tag_configure("blue_text", foreground="black")

                                close_dialog()

                        else:
                            print("FAILED Update")

            # Submit Button
            submit_button = ttk.Button(edit_dialog, text="Edit", command=edit_tag)
            submit_button.grid(row=15, column=0, pady=10)  # Adjusted row position

            # Cancel Button
            submit_button = ttk.Button(edit_dialog, text="Cancel", command=close_dialog)
            submit_button.grid(row=15, column=1, pady=10)


            selected_item = data_tree.focus()
            if selected_item:
                edit_toggle_shift()
                edit_toggle_batch_throw()

                item = data_tree.item(selected_item)['values']
                selected_page_id = item[0]
                selected_sched_start_date = item[9]  # Index of input_start_schedule_date in your data tree
                selected_sched_time = item[10]
                selected_tag_name = item[4]

                # Construct the key
                key = (str(selected_page_id), selected_sched_start_date, selected_sched_time)

                print(key)
                print("Schedulesssssss", scheduled_tag_jobs)

                # Check if the key exists in the dictionary
                if key in scheduled_tag_jobs:
                    #Retrived Data in Scheduled Tag
                    scheduled_job_info = scheduled_tag_jobs[key]
                    data_of_scheduled_tag = scheduled_job_info["data"]

                    edit_page_id_entry.delete(0, tk.END)
                    edit_page_id_entry.insert(0, str(data_of_scheduled_tag["page_id"]))
                    edit_access_token_entry.delete(0, tk.END)
                    edit_access_token_entry.insert(0, str(data_of_scheduled_tag["access_token"]))
                    edit_num_iterations_entry.delete(0, tk.END)
                    edit_num_iterations_entry.insert(0, str(data_of_scheduled_tag["num_iterations"]))
                    edit_max_workers_entry.delete(0, tk.END)
                    edit_max_workers_entry.insert(0, str(data_of_scheduled_tag["max_workers"]))
                    edit_tag_id_to_add_entry.delete(0, tk.END)
                    edit_tag_id_to_add_entry.insert(0, str(data_of_scheduled_tag["tag_id_name"]))

                    if edit_tag_id_to_add_entry.get() !=  str(selected_tag_name):
                        print("notsame")
                        edit_tag_id_to_add_entry.delete(0, tk.END)
                        edit_tag_id_to_add_entry.insert(0, selected_tag_name)
                    
                    get_int_shift = str(data_of_scheduled_tag["shift"])
                    get_int_firstFF = str(data_of_scheduled_tag["on_batch1"])
                    get_int_secondFF = str(data_of_scheduled_tag["on_batch2"])
                    get_int_thirdFF = str(data_of_scheduled_tag["on_batch3"])

                    edit_shift_var.set(int(get_int_shift))
                    edit_first_ff_var.set(int(get_int_firstFF))
                    edit_second_ff_var.set(int(get_int_secondFF))
                    edit_third_ff_var.set(int(get_int_thirdFF))
                    if str(data_of_scheduled_tag["batch_throw"]) == "0":
                        edit_custom_ff_var.set(1)
                    else:
                        edit_custom_ff_var.set(0)

                    edit_toggle_shift()
                    edit_toggle_batch_throw()

                    edit_input_start_date_entry.delete(0, tk.END)
                    edit_input_start_date_entry.insert(0, str(data_of_scheduled_tag["input_start_date"]))
                    edit_input_end_date_entry.delete(0, tk.END)
                    edit_input_end_date_entry.insert(0, str(data_of_scheduled_tag["input_end_date"]))

                    #Input old data conversation time
                    edit_input_start_hour_combobox.set(str(data_of_scheduled_tag["input_start_hour"]))
                    edit_input_start_minute_combobox.set(str(data_of_scheduled_tag["input_start_minute"]))
                    edit_input_start_second_combobox.set(str(data_of_scheduled_tag["input_start_second"]))
                    edit_input_end_hour_combobox.set(str(data_of_scheduled_tag["input_end_hour"]))
                    edit_input_end_minute_combobox.set(str(data_of_scheduled_tag["input_end_minute"]))
                    edit_input_end_second_combobox.set(str(data_of_scheduled_tag["input_end_second"]))

                    edit_input_start_schedule_date_entry.set_date(str(data_of_scheduled_tag["input_start_schedule_date"]))
                    edit_input_end_schedule_date_entry.set_date(str(data_of_scheduled_tag["input_end_schedule_date"]))
                    edit_input_schedule_pattern_combobox.set(str(data_of_scheduled_tag["scheduled_pattern"]))
                    
                    edit_input_schedule_hour_combobox.set(str(data_of_scheduled_tag["schedule_hour"]))
                    edit_input_schedule_minute_combobox.set(str(data_of_scheduled_tag["schedule_minute"]))
                    edit_input_schedule_ampm_combobox.set(str(data_of_scheduled_tag["schedule_ampm"]))
                    edit_input_schedule_hour_combobox2.set(str(data_of_scheduled_tag["schedule_hour"]))
                    edit_input_schedule_minute_combobox2.set(str(data_of_scheduled_tag["schedule_minute"]))
                    edit_input_schedule_ampm_combobox2.set(str(data_of_scheduled_tag["schedule_ampm"]))
                    edit_input_schedule_hour_combobox3.set(str(data_of_scheduled_tag["schedule_hour"]))
                    edit_input_schedule_minute_combobox3.set(str(data_of_scheduled_tag["schedule_minute"]))
                    edit_input_schedule_ampm_combobox3.set(str(data_of_scheduled_tag["schedule_ampm"]))

                    edit_toggle_schedule()
               
                

#Function to Stop selected Schedule
def stop_scheduled_tag():
    selected_item = data_tree.focus()
    if selected_item:
        item = data_tree.item(selected_item)['values']
        selected_page_id = item[0]
        selected_sched_start_date = item[9]  # Index of input_start_schedule_date in your data tree
        selected_sched_time = item[10]  # Index of scheduled_time2 in your data tree
        selected_pattern = item[14]

        if selected_pattern == "Immediately Run":
            messagebox.showerror("Error", "Unable to Stopped. This is not a Scheduled Tag.")
        else:
            # Construct the key
            key = (str(selected_page_id), selected_sched_start_date, selected_sched_time)

            print(key)
            print(item)
            print(scheduled_tag_jobs)
            
            # Check if the key exists in the dictionary
            if key in scheduled_tag_jobs:
                scheduled_job_info = scheduled_tag_jobs[key]
                job = scheduled_job_info["job"]

                # Cancel the scheduled job using the constructed key
                schedule.cancel_job(job)
                del scheduled_tag_jobs[key]
                print("STOP")
                # Update the status in your data tree
                data_tree.set(selected_item, "Status", "Stop")
            else:
                print("FAILED STOP")

# Function to toggle the state of the submit button, schedule date, and schedule time entry widgets based on radio button selection
def toggle_auto_run():
    if auto_run_var.get() == 1:
        submit_button.config(state="normal")  # Enable submit button
        input_start_schedule_date_entry.config(state="disabled")  # Disable schedule date entry
        input_end_schedule_date_entry.config(state="disabled")  # Disable schedule date entry
        input_schedule_hour_combobox.config(state="disabled")  # Disable schedule hour combobox
        input_schedule_minute_combobox.config(state="disabled")  # Disable schedule minute combobox
        input_schedule_ampm_combobox.config(state="disabled")  # Disable schedule AM/PM combobox
        input_schedule_hour_combobox2.config(state="disabled")
        input_schedule_minute_combobox2.config(state="disabled")
        input_schedule_ampm_combobox2.config(state="disabled")
        input_schedule_hour_combobox3.config(state="disabled")
        input_schedule_minute_combobox3.config(state="disabled")
        input_schedule_ampm_combobox3.config(state="disabled")
        input_schedule_pattern_combobox.config(state="disabled")
        input_weekly_pattern_combobox.config(state="disabled")
    else:
        submit_button.config(state="normal")  # Enable submit button
        input_start_schedule_date_entry.config(state="normal")  # Enable schedule date entry
        input_end_schedule_date_entry.config(state="normal")  # Enable schedule date entry
        input_schedule_hour_combobox.config(state="normal")  # Enable schedule hour combobox
        input_schedule_minute_combobox.config(state="normal")  # Enable schedule minute combobox
        input_schedule_ampm_combobox.config(state="normal")  # Enable schedule AM/PM combobox
        input_schedule_hour_combobox2.config(state="normal")
        input_schedule_minute_combobox2.config(state="normal")
        input_schedule_ampm_combobox2.config(state="normal")
        input_schedule_hour_combobox3.config(state="normal")
        input_schedule_minute_combobox3.config(state="normal")
        input_schedule_ampm_combobox3.config(state="normal")
        input_schedule_pattern_combobox.config(state="normal")
        input_weekly_pattern_combobox.config(state="normal")
        
# Function to toggle the state of Shifts
def toggle_shift():
    if shift_var.get() == 1:
        first_ff_checkbox.config(text="1st Throw (3 days ago)", state="normal")
        second_ff_checkbox.config(text="2nd Throw(10 days ago)", state="normal")
        third_ff_checkbox.config(text="3rd Throw(30 days ago)", state="normal")
        custom_ff_checkbox.config(state="normal")
    else:
        first_ff_checkbox.config(text="1st Throw (today @ 5PM)", state="normal")
        second_ff_checkbox.config(text="2nd Throw (today @ 8PM)", state="normal")
        third_ff_checkbox.config(text="3rd Throw (today @ 12MN/AM)", state="normal")
        custom_ff_checkbox.config(state="normal")

#Function to toggle the state of Batches
def toggle_batch_throw():
    if first_ff_var.get() == 1 or second_ff_var.get() == 1 or third_ff_var.get() == 1:
        custom_ff_var.set(0)
        input_start_date_entry.config(state="disabled")
        input_end_date_entry.config(state="disabled")
        input_start_hour_combobox.config(state="disabled")
        input_start_minute_combobox.config(state="disabled")
        input_start_second_combobox.config(state="disabled")
        input_end_hour_combobox.config(state="disabled")
        input_end_minute_combobox.config(state="disabled")
        input_end_second_combobox.config(state="disabled")
        
        input_start_date_label.grid_forget()
        input_end_date_label.grid_forget()
        input_end_date_entry.grid_forget()
        input_start_date_entry.grid_forget()
        end_time_frame.grid_forget()
        time_frame.grid_forget()
        input_start_time_label.grid_forget()
        input_end_time_label.grid_forget()


        if third_ff_var.get() == 1 and second_ff_var.get() == 1 and first_ff_var.get() == 1:
            on_batch1 = 1
            on_batch2 = 1
            on_batch3 = 1

            if shift_var.get() == 0:
                first_sched1.grid(row=0, column=1, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                first_sched.grid(row=0, column=4, sticky=tk.W)
                second_sched.grid(row=1, column=4, sticky=tk.W)
                second_sched1.grid(row=1, column=1, sticky=tk.W)
                third_sched1.grid(row=2, column=1, sticky=tk.W) 

                input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                third_sched.grid(row=2, column=4, sticky=tk.W)
                input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()

        elif third_ff_var.get() == 0 and second_ff_var.get() == 1 and first_ff_var.get() == 1:
            on_batch1 = 1
            on_batch2 = 1
            on_batch3 = 0

            if shift_var.get() == 0:
                first_sched1.grid(row=0, column=1, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                second_sched.grid(row=1, column=4, sticky=tk.W)
                second_sched1.grid(row=1, column=1, sticky=tk.W)
                first_sched.grid(row=0, column=4, sticky=tk.W)

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()

        elif third_ff_var.get() == 1 and second_ff_var.get() == 0 and first_ff_var.get() == 1:
            on_batch1 = 1
            on_batch2 = 0
            on_batch3 = 1

            if shift_var.get() == 0:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)
                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid(row=0, column=4, sticky=tk.W)
                second_sched.grid_forget()
                second_sched1.grid_forget()
                
                third_sched1.grid(row=2, column=1, sticky=tk.W) 
                input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                third_sched.grid(row=2, column=4, sticky=tk.W)
                input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()

        elif third_ff_var.get() == 1 and second_ff_var.get() == 1 and first_ff_var.get() == 0:
            on_batch1 = 0
            on_batch2 = 1
            on_batch3 = 1

            if shift_var.get() == 0:
                first_sched.grid_forget()
                first_sched1.grid_forget()
                input_schedule_hour_combobox.grid_forget()
                input_schedule_minute_combobox.grid_forget()
                input_schedule_ampm_combobox.grid_forget()

                input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                second_sched.grid(row=1, column=4, sticky=tk.W)
                second_sched1.grid(row=1, column=1, sticky=tk.W)

                third_sched1.grid(row=2, column=1, sticky=tk.W) 
                input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                third_sched.grid(row=2, column=4, sticky=tk.W)
                input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()

        elif third_ff_var.get() == 0 and second_ff_var.get() == 0 and first_ff_var.get() == 1:
            on_batch1 = 1
            on_batch2 = 0
            on_batch3 = 0

            if shift_var.get() == 0:
                first_sched.grid_forget()
                first_sched1.grid(row=0, column=1, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()

                third_sched1.grid_forget()
                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()

        elif third_ff_var.get() == 1 and second_ff_var.get() == 0 and first_ff_var.get() == 0:
            on_batch1 = 0
            on_batch2 = 0
            on_batch3 = 1
            
            if shift_var.get() == 0:
                first_sched1.grid_forget()
                input_schedule_hour_combobox.grid_forget()
                input_schedule_minute_combobox.grid_forget()
                input_schedule_ampm_combobox.grid_forget()
                first_sched.grid_forget()

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()

                third_sched1.grid(row=2, column=1, sticky=tk.W) 
                input_schedule_hour_combobox3.grid(row=2, column=0, sticky=tk.W)
                third_sched.grid(row=2, column=4, sticky=tk.W)
                input_schedule_minute_combobox3.grid(row=2, column=2, sticky=tk.W)
                input_schedule_ampm_combobox3.grid(row=2, column=3, sticky=tk.W)
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()

        elif third_ff_var.get() == 0 and second_ff_var.get() == 1 and first_ff_var.get() == 0:
            on_batch1 = 0
            on_batch2 = 1
            on_batch3 = 0

            if shift_var.get() == 0:
                first_sched1.grid_forget()
                input_schedule_hour_combobox.grid_forget()
                input_schedule_minute_combobox.grid_forget()
                input_schedule_ampm_combobox.grid_forget()
                first_sched.grid_forget()

                input_schedule_hour_combobox2.grid(row=1, column=0, sticky=tk.W) 
                input_schedule_minute_combobox2.grid(row=1, column=2, sticky=tk.W) 
                input_schedule_ampm_combobox2.grid(row=1, column=3, sticky=tk.W)
                second_sched.grid(row=1, column=4, sticky=tk.W)
                second_sched1.grid(row=1, column=1, sticky=tk.W)

                third_sched1.grid_forget()
                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()
            else:
                first_sched1.grid(row=0, column=4, sticky=tk.W)
                input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
                input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
                input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

                input_schedule_hour_combobox2.grid_forget()
                input_schedule_minute_combobox2.grid_forget()
                input_schedule_ampm_combobox2.grid_forget()
                first_sched.grid_forget()
                second_sched.grid_forget()
                second_sched1.grid_forget()
                third_sched1.grid_forget()

                input_schedule_hour_combobox3.grid_forget()
                third_sched.grid_forget()
                input_schedule_minute_combobox3.grid_forget()
                input_schedule_ampm_combobox3.grid_forget()
        else:
            first_sched1.grid(row=0, column=4, sticky=tk.W)
            input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)
            input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)
            input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)

            input_schedule_hour_combobox2.grid_forget()
            input_schedule_minute_combobox2.grid_forget()
            input_schedule_ampm_combobox2.grid_forget()
            first_sched.grid_forget()
            second_sched.grid_forget()
            second_sched1.grid_forget()
            third_sched1.grid_forget()

            input_schedule_hour_combobox3.grid_forget()
            third_sched.grid_forget()
            input_schedule_minute_combobox3.grid_forget()
            input_schedule_ampm_combobox3.grid_forget()


        if third_ff_var.get() == 1:
            # first_ff_var.set(1)
            # second_ff_var.set(1)

            #Check Shift
            if shift_var.get() == 1:
                #Get Date from remaining days of this month up to yesterday (AM)
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                
                shift = 1
                batch_throw = 3
                
                changed_schedule_hour = input_schedule_hour_combobox.get()
                changed_schedule_minute = input_schedule_minute_combobox.get()
                changed_schedule_ampm = input_schedule_ampm_combobox.get()
                changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
                
                return start_date, end_date , start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3
            else:
                #Get(PM)
                start_date = datetime.now().strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                
                changed_schedule_hour = input_schedule_hour_combobox.get()
                changed_schedule_minute = input_schedule_minute_combobox.get()
                changed_schedule_ampm = input_schedule_ampm_combobox.get()
                changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
            
                input_schedule_hour_var3.set("12")
                input_schedule_minute_var3.set("00")
                input_schedule_ampm_var3.set("AM")
                
                shift = 0
                batch_throw = 3
         
                return start_date, end_date, start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3
        
        elif second_ff_var.get()==1:
            # first_ff_var.set(1)
            # third_ff_var.set(0)
            #Check Shift
            on_batch2 = 1

            if shift_var.get() == 1:
                #Get Date from 10 days ago up to yesterday (AM)
                start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
                end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                
                shift = 1
                batch_throw = 2
                
                changed_schedule_hour = input_schedule_hour_combobox.get()
                changed_schedule_minute = input_schedule_minute_combobox.get()
                changed_schedule_ampm = input_schedule_ampm_combobox.get()
                changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
                
                return start_date, end_date, start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3
            else:
                #Get Date from 10 days ago up to today (PM)
                start_date = datetime.now().strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                
                changed_schedule_hour = input_schedule_hour_combobox.get()
                changed_schedule_minute = input_schedule_minute_combobox.get()
                changed_schedule_ampm = input_schedule_ampm_combobox.get()
                changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
                
                input_schedule_hour_var2.set("08")
                input_schedule_minute_var2.set("00")
                input_schedule_ampm_var2.set("PM")
                
                shift = 0
                batch_throw = 2
                
                return start_date, end_date, start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3

        elif first_ff_var.get()==1:
            # second_ff_var.set(0)
            # third_ff_var.set(0)
            
            if shift_var.get() == 1:
                # Get the date from three days ago up to yesterday(AM)
                start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
                end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                
                shift = 1
                batch_throw = 1
                
                changed_schedule_hour = input_schedule_hour_combobox.get()
                changed_schedule_minute = input_schedule_minute_combobox.get()
                changed_schedule_ampm = input_schedule_ampm_combobox.get()
                changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
     
                return start_date, end_date, start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3
            else:
                # Get the date from three days ago up to today(PM)
                start_date = datetime.now().strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                
                changed_schedule_hour = input_schedule_hour_combobox.get()
                changed_schedule_minute = input_schedule_minute_combobox.get()
                changed_schedule_ampm = input_schedule_ampm_combobox.get()
                changed_schedule_hour2 = input_schedule_hour_combobox2.get()
                changed_schedule_minute2 = input_schedule_minute_combobox2.get()
                changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
                changed_schedule_hour3 = input_schedule_hour_combobox3.get()
                changed_schedule_minute3 = input_schedule_minute_combobox3.get()
                changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
                
                input_schedule_hour_var.set("05")
                input_schedule_minute_var.set("00")
                input_schedule_ampm_var.set("PM")
                
                shift = 0
                batch_throw = 1
       
                return start_date, end_date, start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3
            
    elif custom_ff_var.get() == 1:
        on_batch1 = 0
        on_batch2 = 0
        on_batch3 = 0
        first_ff_var.set(0)
        second_ff_var.set(0)
        third_ff_var.set(0)
        input_start_date_entry.config(state="normal")
        input_end_date_entry.config(state="normal")
        input_start_hour_combobox.config(state="readonly")
        input_start_minute_combobox.config(state="readonly")
        input_start_second_combobox.config(state="readonly")
        input_end_hour_combobox.config(state="readonly")
        input_end_minute_combobox.config(state="readonly")
        input_end_second_combobox.config(state="readonly")
        
        input_start_date_label.grid(row=8, column=1, sticky=tk.W)
        input_end_date_label.grid(row=9, column=1, sticky=tk.W)
        input_end_date_entry.grid(row=9, column=2, sticky=tk.W)
        input_start_date_entry.grid(row=8, column=2, sticky=tk.W)
        end_time_frame.grid(row=11, column=2, columnspan=6, sticky=tk.W, pady=4)
        time_frame.grid(row=10, column=2, columnspan=6, sticky=tk.W, pady=4)
        input_start_time_label.grid(row=10, column=1, sticky=tk.W)
        input_end_time_label.grid(row=11, column=1, sticky=tk.W)
        
        start_date = input_start_date_entry.get()
        end_date = input_end_date_entry.get()
        start_hour = input_start_hour_combobox.get()
        start_minute = input_start_minute_combobox.get()
        start_seconds = input_start_second_combobox.get()
        end_hour = input_end_hour_combobox.get()
        end_minute = input_end_minute_combobox.get()
        end_seconds = input_end_second_combobox.get()
        
        changed_schedule_hour = input_schedule_hour_combobox.get()
        changed_schedule_minute = input_schedule_minute_combobox.get()
        changed_schedule_ampm = input_schedule_ampm_combobox.get()
        changed_schedule_hour2 = input_schedule_hour_combobox2.get()
        changed_schedule_minute2 = input_schedule_minute_combobox2.get()
        changed_schedule_ampm2 = input_schedule_ampm_combobox2.get()
        changed_schedule_hour3 = input_schedule_hour_combobox3.get()
        changed_schedule_minute3 = input_schedule_minute_combobox3.get()
        changed_schedule_ampm3 = input_schedule_ampm_combobox3.get()
        
        shift = 2
        batch_throw = 0
        
        return start_date, end_date, start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3
    
    elif custom_ff_var.get() == 0:
        input_start_date_entry.config(state="disabled")
        input_end_date_entry.config(state="disabled")
        input_start_hour_combobox.config(state="disabled")
        input_start_minute_combobox.config(state="disabled")
        input_start_second_combobox.config(state="disabled")
        input_end_hour_combobox.config(state="disabled")
        input_end_minute_combobox.config(state="disabled")
        input_end_second_combobox.config(state="disabled")
        
        input_start_date_label.grid_forget()
        input_end_date_label.grid_forget()
        input_end_date_entry.grid_forget()
        input_start_date_entry.grid_forget()
        end_time_frame.grid_forget()
        time_frame.grid_forget()
        input_start_time_label.grid_forget()
        input_end_time_label.grid_forget()

#Set Schedule Pattern
def toggle_schedule(event):
    selected_pattern = input_schedule_pattern_var.get()
    if selected_pattern == "Once":
        input_end_schedule_date_entry.set_date(input_start_schedule_date_entry.get())
        input_weekly_pattern_combobox.grid_forget()
        weekly_label.grid_forget()
    elif selected_pattern == "Weekly":
        weekly_label.grid(row=0, column=6, sticky=tk.W)
        input_weekly_pattern_combobox.grid(row=0, column=7, sticky=tk.W)
    else:
        input_weekly_pattern_combobox.grid_forget()
        weekly_label.grid_forget()

# Function to run the scheduler in a separate thread
def run_scheduler():
    def _run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Check if the scheduler is already running
    if not any(t.name == '_run_scheduler' for t in threading.enumerate()):
        # Start the scheduler in a separate thread if it's not already running
        threading.Thread(target=_run_scheduler, daemon=True, name='_run_scheduler').start()
        

# Call run_scheduler() to start the scheduler
run_scheduler()

def extract_part(tag):
    day_str = tag[3:5]
    
    # Converting day string to integer
    try:
        day = int(day_str)
    except ValueError:
        try:
            day_str = tag[3:4]
            day = int(day_str)
        except ValueError:
            return "False"
    
    if day < 9:
        prefix_length = 4
    else:
        prefix_length = 5 

    return tag[prefix_length:]

def toggle_schedule_entry_widgets(input_start_schedule_date_entry,input_end_schedule_date_entry, input_schedule_hour_combobox, input_schedule_minute_combobox, input_schedule_ampm_combobox, input_schedule_hour_combobox2, input_schedule_minute_combobox2, input_schedule_ampm_combobox2, input_schedule_hour_combobox3, input_schedule_minute_combobox3, input_schedule_ampm_combobox3):
    if auto_run_var.get() == 1:
        input_start_schedule_date_entry.config(state="disabled")
        input_end_schedule_date_entry.config(state="disabled")
        input_schedule_hour_combobox.config(state="disabled")
        input_schedule_minute_combobox.config(state="disabled")
        input_schedule_ampm_combobox.config(state="disabled")
        input_schedule_hour_combobox2.config(state="disabled")
        input_schedule_minute_combobox2.config(state="disabled")
        input_schedule_ampm_combobox2.config(state="disabled")
        input_schedule_hour_combobox3.config(state="disabled")
        input_schedule_minute_combobox3.config(state="disabled")
        input_schedule_ampm_combobox3.config(state="disabled")
        input_schedule_pattern_combobox.config(state="disabled")
        input_weekly_pattern_combobox.config(state="disabled")
    else:
        input_start_schedule_date_entry.config(state="normal")
        input_end_schedule_date_entry.config(state="normal")
        input_schedule_hour_combobox.config(state="normal")
        input_schedule_minute_combobox.config(state="normal")
        input_schedule_ampm_combobox.config(state="normal")
        input_schedule_hour_combobox2.config(state="normal")
        input_schedule_minute_combobox2.config(state="normal")
        input_schedule_ampm_combobox2.config(state="normal")
        input_schedule_hour_combobox3.config(state="normal")
        input_schedule_minute_combobox3.config(state="normal")
        input_schedule_ampm_combobox3.config(state="normal")
        input_schedule_pattern_combobox.config(state="normal")
        input_weekly_pattern_combobox.config(state="normal")


def toggle_tag_for_from_id(args):
    from_id, page_id, access_token, tag_id_to_add, running_data_text, progress_bar = args  # Update function signature to include progress_bar
    
    #List of unique conversation ID
    global unique_conv_id
    conversation_id = f"{page_id}_{from_id}"
    
    #Check if Conversation ID already mentioned
    if from_id not in unique_conv_id:
        unique_conv_id.append(from_id)
        
        # Construct the message with counter
        message = f"#{toggle_tag_for_from_id.counter} Tagged conversation: {conversation_id}\n"
        toggle_tag_for_from_id.counter += 1
    
        # Print the message to the UI
        running_data_text.insert(tk.END, message)
        running_data_text.yview(tk.END)

        # Construct the URL for toggling tags
        toggle_tag_url = f"https://pancake.ph/api/v1/pages/{page_id}/conversations/{conversation_id}/toggle_tag?access_token={access_token}"

        # Payload for the POST request with from_id
        payload = {
            "tag_id": tag_id_to_add,
            "value": 1,
            "psid": from_id,  # Assuming PSID is obtained from the 'id' field
            "tag[color]": "#0d5aff",
            "tag[id]": tag_id_to_add,
            "tag[lighten_color]": "#b6cdff",
            "tag[text]": "Urgent"
        }

        # Send POST request
        headers = {}
        try:
            response = requests.request("POST", toggle_tag_url, headers=headers, data=payload)

            # Check response status
            if response.status_code == 200:
                # Update progress bar value
                # progress_bar["value"] += 1
                return True # Return True for successful tagging
            else:
                return False # Return False for unsuccessful tagging
        except requests.exceptions.ReadTimeout:
            try: 
                response = requests.request("POST", toggle_tag_url, headers=headers, data=payload)

                # Check response status
                if response.status_code == 200:
                    # Update progress bar value
                    # progress_bar["value"] += 1
                    return True # Return True for successful tagging
                else:
                    return False # Return False for unsuccessful tagging
            except requests.exceptions.ReadTimeout:
                messagebox.showerror("Connection Timeout", "Failed to connect to the server. Please check your internet connection or the page. Try again later.")
                return False
           
toggle_tag_for_from_id.counter = 1  # Initialize the counter
unique_conv_id = [] #form Id/Conversational ID List


# Function to retrieve tag info based on tag name
def get_tag_info(tag_name, api_url):
    try:
        # Make GET request to the API endpoint
        response = requests.get(api_url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Check if 'settings' key is present in the response
            if 'settings' in data and 'tags' in data['settings']:
                # Iterate through the tags and find the matching tag_name
                for idx, tag in enumerate(data['settings']['tags']):
                    if tag.get('text', '').lower() == tag_name.lower():
                        return idx, tag.get('id')
                
                # If tag_name not found, return None
                return None, None
            else:
                return None, None
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        if e:
            progress_bar_label.config(text="Error")
            idx = "error"
            tag = "time_out"
            return idx, tag

# Function to convert date and time string to datetime object
def combine_date_time(date_str, time_str):
    # Combine date and time strings
    combined_str = f"{date_str} {time_str}"
    print("sdfsdf", combined_str)
    # Parse combined string to datetime object using the appropriate format
    try:
        # Attempt to parse the time string using the original format
        return datetime.strptime(combined_str, "%Y-%m-%d %H:%M")
    except ValueError:
        # If parsing fails, try parsing using the alternative format
        return datetime.strptime(combined_str, "%m/%d/%y %I:%M %p")

# Submit Form
def submit_form():
    
    #Get Conversation Start and End DateTime
    start_date , end_date , start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm, changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3 =  toggle_batch_throw()
    
    # Get form input values
    page_id = page_id_entry.get()
    access_token = access_token_entry.get()
    num_iterations = int(num_iterations_entry.get())
    max_workers = int(max_workers_entry.get())
    tag_id_name = tag_id_to_add_entry.get()
    input_start_date = start_date
    input_end_date = end_date
    input_start_schedule_date = input_start_schedule_date_entry.get()
    input_end_schedule_date = input_end_schedule_date_entry.get()
    shift = shift
    batch_throw = batch_throw
    
    #start conversational time
    input_start_hour = start_hour
    input_start_minute = start_minute
    input_start_second = start_seconds
    input_end_hour = end_hour
    input_end_minute = end_minute
    input_end_second = end_seconds
    #--------------
    
    input_schedule_hour = input_schedule_hour_combobox.get()
    input_schedule_minute = input_schedule_minute_combobox.get()
    input_schedule_ampm = input_schedule_ampm_combobox.get()
    
    #PM 2nd Throw Schedule Time
    input_schedule_hour2 = input_schedule_hour_combobox2.get()
    input_schedule_minute2 = input_schedule_minute_combobox2.get()
    input_schedule_ampm2 = input_schedule_ampm_combobox2.get()
    
    #PM 3rd Throw Schedule Time
    input_schedule_hour3 = input_schedule_hour_combobox3.get()
    input_schedule_minute3 = input_schedule_minute_combobox3.get()
    input_schedule_ampm3 = input_schedule_ampm_combobox3.get()
    
    scheduled_pattern = input_schedule_pattern_combobox.get()
    weekly_pattern = input_weekly_pattern_combobox.get()

    # Combine scheduled date and time into datetime object
    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
    scheduled_datetime = combine_date_time(input_start_schedule_date, scheduled_time)

    scheduled_time2 = f"{input_schedule_hour2}:{input_schedule_minute2} {input_schedule_ampm2}"
    scheduled_datetime2 = combine_date_time(input_start_schedule_date, scheduled_time2)

    scheduled_time3 = f"{input_schedule_hour3}:{input_schedule_minute3} {input_schedule_ampm3}"
    scheduled_datetime3 = combine_date_time(input_start_schedule_date, scheduled_time3)

    if auto_run_var.get() == 1:
        batch = "auto"
        # Run the data immediately in a separate thread (add the start and end time)
        current_time = datetime.now()

        # Extract hour, minute, and AM/PM
        input_schedule_hour = current_time.strftime("%I")  # %I for 12-hour format, %H for 24-hour format
        input_schedule_minute = current_time.strftime("%M")
        input_schedule_ampm = current_time.strftime("%p")
        scheduled_pattern = "Run Immediately"

        threading.Thread(target=execute_task, args=(page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)).start()
        update_table(batch)
    else:
        #Run the data in set Schedule
        #PM Shift
        if shift == 0:
            for batch_pmff_throw in range(batch_throw):
                batch_throw_no = batch_pmff_throw+1
                if batch_throw_no == 1 and on_batch1 == 1:
                    batch = "1"
                    batch_throw = 1
                    if changed_schedule_hour != "05" or changed_schedule_minute != "00" or changed_schedule_ampm != "PM":
                        schedule_hour = changed_schedule_hour
                        schedule_minute = changed_schedule_minute
                        schedule_ampm = changed_schedule_ampm
                        input_schedule_hour_var.set(schedule_hour)
                        input_schedule_minute_var.set(schedule_minute)
                        input_schedule_ampm_var.set(schedule_ampm)

                        if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                            scheduled_time1 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            scheduled_datetime1 = combine_date_time(input_start_schedule_date, scheduled_time1)
                            scheduled_time1 = scheduled_datetime1.strftime("%H:%M")
                            job = schedule.every().day.at(scheduled_time1).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            # This is for Filter stop and edit Schedule
                            schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"

                            # Store entire data set associated with scheduled job
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": None,
                                "on_batch1": 1,
                                "on_batch2": 0,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time4] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            print("batch1", scheduled_tag_jobs)
                            
                            # Update the table with the form data
                            update_table(batch)

                        else:
                            # Define a dictionary mapping days of the week to their corresponding method
                            day_to_method = {
                                'Monday': schedule.every().monday,
                                'Tuesday': schedule.every().tuesday,
                                'Wednesday': schedule.every().wednesday,
                                'Thursday': schedule.every().thursday,
                                'Friday': schedule.every().friday,
                                'Saturday': schedule.every().saturday,
                                'Sunday': schedule.every().sunday
                            }
                                
                            week_day = weekly_pattern
                            print(week_day)
                                
                            scheduled_time1 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            scheduled_datetime1 = combine_date_time(input_start_schedule_date, scheduled_time1)
                            scheduled_time1 = scheduled_datetime1.strftime("%H:%M")
                            job = day_to_method[week_day].at(scheduled_time1).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            
                            #Save data of schedule (for stop and ediy schedule)
                            schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            data_of_scheduled_tag = schedule_time4, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3
                            scheduled_tag_jobs[data_of_scheduled_tag] = job
                            print("batch1:weekly", scheduled_tag_jobs)
                            schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"

                            # Store entire data set associated with scheduled job
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": week_day,
                                "on_batch1": 1,
                                "on_batch2": 0,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time4] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            
                            # Update the table with the form data
                            update_table(batch)
                    else:
                        input_schedule_hour = input_schedule_hour_combobox.get()
                        input_schedule_minute = input_schedule_minute_combobox.get()
                        input_schedule_ampm = input_schedule_ampm_combobox.get()

                        if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                            scheduled_time = scheduled_datetime.strftime("%H:%M")
                            job = schedule.every().day.at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            # This is for Filter stop and edit Schedule
                            schedule_time4 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": input_schedule_hour,
                                "schedule_minute": input_schedule_minute,
                                "schedule_ampm": input_schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": None,
                                "on_batch1": 1,
                                "on_batch2": 0,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time4] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            # Update the table with the form data
                            update_table(batch)

                        else:
                            # Define a dictionary mapping days of the week to their corresponding method
                            day_to_method = {
                                'Monday': schedule.every().monday,
                                'Tuesday': schedule.every().tuesday,
                                'Wednesday': schedule.every().wednesday,
                                'Thursday': schedule.every().thursday,
                                'Friday': schedule.every().friday,
                                'Saturday': schedule.every().saturday,
                                'Sunday': schedule.every().sunday
                            }
                                
                            week_day = weekly_pattern
                                
                            scheduled_time = scheduled_datetime.strftime("%H:%M")
                            job = day_to_method[week_day].at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            
                            schedule_time4 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            data_of_scheduled_tag = schedule_time4, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3
                            scheduled_tag_jobs[data_of_scheduled_tag] = job
                            print("batch1:weekly", scheduled_tag_jobs)
                            schedule_time4 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"

                            # Store entire data set associated with scheduled job
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": week_day,
                                "on_batch1": 1,
                                "on_batch2": 0,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time4] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            # Update the table with the form data
                            update_table(batch)

                elif batch_throw_no == 2 and on_batch2 == 1:
                    batch = "2"
                    batch_throw = 2
                    if changed_schedule_hour2 != "08" or changed_schedule_minute2 != "00" or changed_schedule_ampm2 != "PM":
                        schedule_hour = changed_schedule_hour2
                        schedule_minute = changed_schedule_minute2
                        schedule_ampm = changed_schedule_ampm2
                        input_schedule_hour_var2.set(schedule_hour)
                        input_schedule_minute_var2.set(schedule_minute)
                        input_schedule_ampm_var2.set(schedule_ampm)
                        if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                            scheduled_time2 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            scheduled_datetime2 = combine_date_time(input_start_schedule_date, scheduled_time2)
                            scheduled_time = scheduled_datetime2.strftime("%H:%M")

                            job = schedule.every().day.at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            # This is for Filter stop and edit Schedule
                            schedule_time5 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": None,
                                "on_batch1": 0,
                                "on_batch2": 1,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time5] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            print("batch2",scheduled_tag_jobs)
                            print("------batch2", job, "-------------------")
                            # Update the table with the form data
                            update_table(batch)

                        else:
                            # Define a dictionary mapping days of the week to their corresponding method
                            day_to_method = {
                                'Monday': schedule.every().monday,
                                'Tuesday': schedule.every().tuesday,
                                'Wednesday': schedule.every().wednesday,
                                'Thursday': schedule.every().thursday,
                                'Friday': schedule.every().friday,
                                'Saturday': schedule.every().saturday,
                                'Sunday': schedule.every().sunday
                            }
                                
                            week_day = weekly_pattern
                                
                            scheduled_time2 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            scheduled_datetime2 = combine_date_time(input_start_schedule_date, scheduled_time2)
                            scheduled_time = scheduled_datetime2.strftime("%H:%M")
                            job = day_to_method[week_day].at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour2, input_schedule_minute2, input_schedule_ampm2, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            
                            schedule_time5 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": week_day,
                                "on_batch1": 0,
                                "on_batch2": 1,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time5] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            # Update the table with the form data
                            update_table(batch)
                    else:
                        input_schedule_hour = input_schedule_hour_combobox2.get()
                        input_schedule_minute = input_schedule_minute_combobox2.get()
                        input_schedule_ampm = input_schedule_ampm_combobox2.get()

                        if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                            scheduled_time = scheduled_datetime2.strftime("%H:%M")
                            job = schedule.every().day.at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            schedule_time5 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time5] = job
                            
                            schedule_time5 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": input_schedule_hour,
                                "schedule_minute": input_schedule_minute,
                                "schedule_ampm": input_schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": None,
                                "on_batch1": 0,
                                "on_batch2": 1,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time5] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }
                            
                            print("batch2",scheduled_tag_jobs)
                            print("------batch2", job, "-------------------")
                            # Update the table with the form data
                            update_table(batch)

                        else:
                            # Define a dictionary mapping days of the week to their corresponding method
                            day_to_method = {
                                'Monday': schedule.every().monday,
                                'Tuesday': schedule.every().tuesday,
                                'Wednesday': schedule.every().wednesday,
                                'Thursday': schedule.every().thursday,
                                'Friday': schedule.every().friday,
                                'Saturday': schedule.every().saturday,
                                'Sunday': schedule.every().sunday
                            }
                                
                            week_day = weekly_pattern
                                
                            scheduled_time = scheduled_datetime2.strftime("%H:%M")
                            day_to_method[week_day].at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            
                            schedule_time5 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": input_schedule_hour,
                                "schedule_minute": input_schedule_minute,
                                "schedule_ampm": input_schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": week_day,
                                "on_batch1": 0,
                                "on_batch2": 1,
                                "on_batch3": 0
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time5] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }
                            
                            # Update the table with the form data
                            update_table(batch)

                elif batch_throw_no == 3 and on_batch3 == 1:
                    batch = "3"
                    batch_throw = 3
                    if changed_schedule_hour3 != "12" or changed_schedule_minute3 != "00" or changed_schedule_ampm3 != "AM":
                        schedule_hour = changed_schedule_hour3
                        schedule_minute = changed_schedule_minute3
                        schedule_ampm = changed_schedule_ampm3
                        input_schedule_hour_var3.set(schedule_hour)
                        input_schedule_minute_var3.set(schedule_minute)
                        input_schedule_ampm_var3.set(schedule_ampm)

                        scheduled_time3 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                        scheduled_datetime3 = combine_date_time(input_start_schedule_date, scheduled_time3)
                        
                        if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                            scheduled_time6 = scheduled_datetime3.strftime("%H:%M")
                            schedule_time6 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            job = schedule.every().day.at(scheduled_time6).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, schedule_hour, schedule_minute, schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = job
                            
                            schedule_time6 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": None,
                                "on_batch1": 0,
                                "on_batch2": 0,
                                "on_batch3": 1
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }

                            # Update the table with the form data
                            update_table(batch)

                        else:
                            # Define a dictionary mapping days of the week to their corresponding method
                            day_to_method = {
                                'Monday': schedule.every().monday,
                                'Tuesday': schedule.every().tuesday,
                                'Wednesday': schedule.every().wednesday,
                                'Thursday': schedule.every().thursday,
                                'Friday': schedule.every().friday,
                                'Saturday': schedule.every().saturday,
                                'Sunday': schedule.every().sunday
                            }
                                
                            week_day = weekly_pattern
                                
                            scheduled_time = scheduled_datetime3.strftime("%H:%M")
                            job = day_to_method[week_day].at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour3, input_schedule_minute3, input_schedule_ampm3, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            
                            schedule_time6 = f"{schedule_hour}:{schedule_minute} {schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": schedule_hour,
                                "schedule_minute": schedule_minute,
                                "schedule_ampm": schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": week_day,
                                "on_batch1": 0,
                                "on_batch2": 0,
                                "on_batch3": 1
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }
                            
                            # Update the table with the form data
                            update_table(batch)
                    else:
                        today = datetime.now().date()
                        # Calculate tomorrow's date
                        tomorrow = today + timedelta(days=1)
                        # Format tomorrow's date as month/day/year
                        formatted_date = tomorrow.strftime("%m/%d/%y").lstrip("0")
                        input_start_schedule_date = formatted_date

                        input_schedule_hour = input_schedule_hour_combobox3.get()
                        input_schedule_minute = input_schedule_minute_combobox3.get()
                        input_schedule_ampm = input_schedule_ampm_combobox3.get()

                        # scheduled_time3 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                        # scheduled_datetime3 = combine_date_time(input_schedule_start_date, scheduled_time3)
                        
                        if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                            scheduled_time = scheduled_datetime3.strftime("%H:%M")
                            schedule_time6 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            job = schedule.every().day.at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = job
                            
                            schedule_time6 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": input_schedule_hour,
                                "schedule_minute": input_schedule_minute,
                                "schedule_ampm": input_schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": None,
                                "on_batch1": 0,
                                "on_batch2": 0,
                                "on_batch3": 1
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }
                            
                            # Update the table with the form data
                            update_table(batch)

                        else:
                            # Define a dictionary mapping days of the week to their corresponding method
                            day_to_method = {
                                'Monday': schedule.every().monday,
                                'Tuesday': schedule.every().tuesday,
                                'Wednesday': schedule.every().wednesday,
                                'Thursday': schedule.every().thursday,
                                'Friday': schedule.every().friday,
                                'Saturday': schedule.every().saturday,
                                'Sunday': schedule.every().sunday
                            }
                                
                            week_day = weekly_pattern
                                
                            scheduled_time = scheduled_datetime3.strftime("%H:%M")
                            job = day_to_method[week_day].at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                            
                            schedule_time6 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            data_of_scheduled_tag = {
                                "page_id": page_id,
                                "access_token": access_token,
                                "num_iterations": num_iterations,
                                "max_workers": max_workers,
                                "tag_id_name": tag_id_name,
                                "input_start_date": input_start_date,
                                "input_end_date": input_end_date,
                                "input_start_hour": input_start_hour,
                                "input_start_minute": input_start_minute,
                                "input_start_second": input_start_second,
                                "input_end_hour": input_end_hour,
                                "input_end_minute": input_end_minute,
                                "input_end_second": input_end_second,
                                "shift": shift,
                                "batch_throw": batch_throw,
                                "input_start_schedule_date": input_start_schedule_date,
                                "schedule_hour": input_schedule_hour,
                                "schedule_minute": input_schedule_minute,
                                "schedule_ampm": input_schedule_ampm,
                                "input_end_schedule_date": input_end_schedule_date,
                                "scheduled_pattern": scheduled_pattern,
                                "weekly_pattern": week_day,
                                "on_batch1": 0,
                                "on_batch2": 0,
                                "on_batch3": 1
                            }


                            scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = {
                                "job": job,
                                "data": data_of_scheduled_tag
                            }
                            
                            # Update the table with the form data
                            update_table(batch)
        else:
            batch = "none"
            # Schedule the task to run at the specified date and time and set schedule pattern()
            if scheduled_pattern == "Everyday" or scheduled_pattern == "Once":
                scheduled_time = scheduled_datetime.strftime("%H:%M")
                schedule_time6 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                job = schedule.every().day.at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
        
                data_of_scheduled_tag = {
                    "page_id": page_id,
                    "access_token": access_token,
                    "num_iterations": num_iterations,
                    "max_workers": max_workers,
                    "tag_id_name": tag_id_name,
                    "input_start_date": input_start_date,
                    "input_end_date": input_end_date,
                    "input_start_hour": input_start_hour,
                    "input_start_minute": input_start_minute,
                    "input_start_second": input_start_second,
                    "input_end_hour": input_end_hour,
                    "input_end_minute": input_end_minute,
                    "input_end_second": input_end_second,
                    "shift": shift,
                    "batch_throw": batch_throw,
                    "input_start_schedule_date": input_start_schedule_date,
                    "schedule_hour": input_schedule_hour,
                    "schedule_minute": input_schedule_minute,
                    "schedule_ampm": input_schedule_ampm,
                    "input_end_schedule_date": input_end_schedule_date,
                    "scheduled_pattern": scheduled_pattern,
                    "weekly_pattern": None,
                    "on_batch1": on_batch1,
                    "on_batch2": on_batch2,
                    "on_batch3": on_batch3
                }


                scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = {
                    "job": job,
                    "data": data_of_scheduled_tag
                }
                print(scheduled_tag_jobs)
                # Update the table with the form data
                update_table(batch)
            else:
                
                # Define a dictionary mapping days of the week to their corresponding method
                day_to_method = {
                    'Monday': schedule.every().monday,
                    'Tuesday': schedule.every().tuesday,
                    'Wednesday': schedule.every().wednesday,
                    'Thursday': schedule.every().thursday,
                    'Friday': schedule.every().friday,
                    'Saturday': schedule.every().saturday,
                    'Sunday': schedule.every().sunday
                }
                
                week_day = weekly_pattern
                
                scheduled_time = scheduled_datetime.strftime("%H:%M")
                job = day_to_method[week_day].at(scheduled_time).do(execute_task, page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3)
                
                schedule_time6 = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                data_of_scheduled_tag = {
                    "page_id": page_id,
                    "access_token": access_token,
                    "num_iterations": num_iterations,
                    "max_workers": max_workers,
                    "tag_id_name": tag_id_name,
                    "input_start_date": input_start_date,
                    "input_end_date": input_end_date,
                    "input_start_hour": input_start_hour,
                    "input_start_minute": input_start_minute,
                    "input_start_second": input_start_second,
                    "input_end_hour": input_end_hour,
                    "input_end_minute": input_end_minute,
                    "input_end_second": input_end_second,
                    "shift": shift,
                    "batch_throw": batch_throw,
                    "input_start_schedule_date": input_start_schedule_date,
                    "schedule_hour": input_schedule_hour,
                    "schedule_minute": input_schedule_minute,
                    "schedule_ampm": input_schedule_ampm,
                    "input_end_schedule_date": input_end_schedule_date,
                    "scheduled_pattern": scheduled_pattern,
                    "weekly_pattern": week_day,
                    "on_batch1": on_batch1,
                    "on_batch2": on_batch2,
                    "on_batch3": on_batch3
                }


                scheduled_tag_jobs[page_id, input_start_schedule_date, schedule_time6] = {
                    "job": job,
                    "data": data_of_scheduled_tag
                }
                
                # Update the table with the form data
                update_table(batch)

        # Start the scheduler in a separate thread
        threading.Thread(target=run_scheduler).start()

        # Toggle the state of the Schedule Date and Time entry widgets
        toggle_schedule_entry_widgets(input_start_schedule_date_entry,input_end_schedule_date_entry, input_schedule_hour_combobox, input_schedule_minute_combobox, input_schedule_ampm_combobox, input_schedule_hour_combobox2, input_schedule_minute_combobox2, input_schedule_ampm_combobox2, input_schedule_hour_combobox3, input_schedule_minute_combobox3, input_schedule_ampm_combobox3)
    # Clear entry labels
    page_id_entry.delete(0, tk.END)
    input_start_date_entry.delete(0, tk.END)
    input_end_date_entry.delete(0, tk.END)
    
    #conversational time
    input_start_hour_combobox.set('')
    input_start_minute_combobox.set('')
    input_start_second_combobox.set('')
    input_end_hour_combobox.set('')
    input_end_minute_combobox.set('')
    input_end_second_combobox.set('')
    #----------
    
    # input_start_schedule_date_entry.delete(0, tk.END)
    # input_schedule_hour_combobox.set('')
    # input_schedule_minute_combobox.set('')
    # input_schedule_ampm_combobox.set('')

# Function to execute the long-running task
def execute_task(page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3):
 
    print(on_batch1, on_batch2, on_batch3)

    # Check Date Range
    check_start_schedule_date = datetime.strptime(input_start_schedule_date, "%m/%d/%y")
    check_end_schedule_date = datetime.strptime(input_end_schedule_date, "%m/%d/%y")
    end_sched = check_end_schedule_date + timedelta(days=1)
    
    if check_start_schedule_date <= datetime.now() <= end_sched:
    
        #reset Terminal
        running_data_text.delete('1.0', tk.END) 
        print("page id", page_id)

        #Generate Tag For Today
        current_time = datetime.now().time()
        current_day = datetime.now().date()
        sched_time_str = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
        sched_time = datetime.strptime(sched_time_str, "%I:%M %p")
        
        #Set Tag for that Day
        if sched_time_str == "12:00 AM":
            current_date = datetime.now()
            current_date = current_date - timedelta(days=1)
        else:
            current_date = datetime.now()

        time_difference = current_date - sched_time
        month = current_date.strftime("%b").upper()  # Get the first 3 letters of the month in uppercase
        day = current_date.strftime("%#d")  # Get the day
        old_tag = tag_id_name
        get_tag_prefix = extract_part(tag_id_name)
        
        if get_tag_prefix == "False":
            tag_id_name = old_tag
        else:
            if time_difference >= timedelta(hours=24):
                tag_id_name = f"{month}{day}{get_tag_prefix}"
            else:
                tag_id_name = old_tag

            items_update_tag = data_tree.get_children()
            for item_update_tag in items_update_tag:
                start_time_update_tag = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                end_time_update_tag = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                                
                scheduled_time_update_tag = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                values3 = data_tree.item(item_update_tag, 'values')

                if values3 and values3[0] == page_id and values3[1] == access_token and values3[4] == old_tag and values3[5] == input_start_date and values3[6] == input_end_date and values3[7] == start_time_update_tag and values3[8] == end_time_update_tag and values3[9] == input_start_schedule_date and values3[10] == scheduled_time_update_tag:
                    data_tree.set(item_update_tag, "Tag Name",tag_id_name )
                    break
        
        if batch_throw == 1 or batch_throw == 2 or batch_throw == 3:
            #Loop of Each Batch Throw
            global unique_conv_id
            total_success_tag = 0
            if shift == 1:
            
                for batch_ff_throw in range(batch_throw):
                    throw = batch_ff_throw+1
                    
                    if throw == 1 and on_batch1 == 1:
                        # Get the date from three days ago up to yesterday(AM)
                        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
                        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                        start_hour = "00"
                        start_minute = "00"
                        start_seconds = "00"
                        end_hour = "23"
                        end_minute = "59"
                        end_seconds = "59"
                        
                        start_datetime = datetime.strptime(f"{start_date} {start_hour}:{start_minute}:{start_seconds}", "%Y-%m-%d %H:%M:%S")
                        start_time = int(start_datetime.timestamp())

                        # Combine end date, hour, minute, and second (with conversational Time)
                        end_datetime = datetime.strptime(f"{end_date} {end_hour}:{end_minute}:{end_seconds}", "%Y-%m-%d %H:%M:%S")
                        end_time = int(end_datetime.timestamp())
                        

                        # API URL to retrieve tag info
                        tag_info_api_url = f"https://pancake.ph/api/v1/pages/{page_id}/settings?access_token={access_token}"

                        # Get the tag_order_id and tag_id_to_add
                        tag_order_id, tag_id_to_add = get_tag_info(tag_id_name, tag_info_api_url)

                        if tag_order_id is not None and tag_id_to_add is not None:
                            # Construct URL with epoch time and tag_order_id (end time edited)
                            initial_url = f"https://pancake.ph/api/v1/pages/{page_id}/conversations?type=NOPHONE,INBOX,CREATE_DATE:{start_time}+-+{end_time}&mode=OR&tags=[]&except_tags=[{tag_order_id}]&access_token={access_token}&from_platform=web"

                            # List to store tagged conversations
                            tagged_conversations = []
                            unique_conversation_id = []
                            # Variable to Store Toral Successful toggles
                            total_successful_toggles = 0
                            
                            # Loop through the process for the specified number of iterations
                            for iteration in range(num_iterations):

                                # Initialize progress bar
                                progress_bar["value"] = iteration
                                progress_bar["maximum"] = num_iterations
                                progress_bar_label.config(text=f"Progress: {iteration+1}%")
                                
                                #Update Data Tree as Ongoing
                                start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                items3 = data_tree.get_children()
                                for item3 in items3:
                                    values3 = data_tree.item(item3, 'values')
                                    if values3 and values3[0] == page_id and values3[1] == access_token and values3[4] == tag_id_name and values3[5] == input_start_date and values3[6] == input_end_date and values3[7] == start_time and values3[8] == end_time and values3[9] == input_start_schedule_date and values3[10] == scheduled_time:
                                        data_tree.set(item3, "Batch", f"1 / {batch_throw}")
                                        data_tree.set(item3, "Status", "Ongoing")  # Update total ongoing toggles
                                        break
                                
                                try:
                                    response = requests.get(initial_url)
                                    data = response.json()
                                except requests.exceptions.JSONDecodeError:
                                    try:
                                        response = requests.get(initial_url)
                                        data = response.json()
                                    except:
                                        #Time Out Error
                                        start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                        end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                        
                                        scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                        
                                        #Update Data Tree
                                        items2 = data_tree.get_children()
                                        for item2 in items2:
                                            values2 = data_tree.item(item2, 'values')
                                            if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                                data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                                                data_tree.set(item2, "Status", "Time Out")
                                                data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                                break

                                        messagebox.showerror("Error", "Invalid Response \n Please Click Ok to continue")
                                except requests.exceptions.RequestException as e:
                                    # Handle other request exceptions
                                    start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                    end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                        
                                    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                        
                                    #Update Data Tree
                                    items2 = data_tree.get_children()
                                    for item2 in items2:
                                        values2 = data_tree.item(item2, 'values')
                                        if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                            data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                                            data_tree.set(item2, "Status", "Lost Connection")
                                            data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                            break

                                    message = f"Request failed: {e}"
                                    messagebox.showerror("Error", message)

                                # Extract the conversations from the initial response
                                conversations = data.get("conversations", [])

                                # Process each conversation to toggle tag using threading
                                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                                    results = executor.map(toggle_tag_for_from_id, [(conv.get("from", {}).get("id"), page_id, access_token, tag_id_to_add, running_data_text, progress_bar) for conv in conversations])
                                    for success, conv_id in zip(results, [conv.get("from", {}).get("id") for conv in conversations]):
                                        # progress_bar["value"] += 1 # Increment total successful toggles
                                        root.update_idletasks()  # Update GUI
                                        if success:
                                            if conv_id not in unique_conversation_id:
                                                total_successful_toggles += 1
                                                tagged_conversations.append(conv_id)
                                                unique_conversation_id.append(conv_id)
                                            else:
                                                print("Already mention")

                            # Update running data text
                            running_data_text.insert(tk.END, f"1st Throw Total successful tag toggles: {total_successful_toggles}\n")
                            running_data_text.yview(tk.END)
                            root.bell()
                            # global unique_conv_id
                            total_success_tag = total_successful_toggles
                            unique_conv_id = []
                            toggle_tag_for_from_id.counter = 1
                            
                            #Filter Start and End Time for Update of Table
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"

                            # Update the status in data_tree to "Done"
                            for conv_id in tagged_conversations:
                                # Find the item in the treeview with matching conversation ID
                                items = data_tree.get_children()
                                for item in items:
                                    
                                    values = data_tree.item(item, 'values')
                                    if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                        data_tree.set(item, "Batch", f"1 / {batch_throw}")
                                        data_tree.set(item, "Status", "Done")
                                        data_tree.set(item, "Total Successful Toggles", total_successful_toggles)  # Update total successful toggles
                                        break
                            
                            #Update Data Tree
                            if total_successful_toggles == 0:
                                items = data_tree.get_children()
                                for item in items:
                                    values = data_tree.item(item, 'values')
                                    if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                        data_tree.set(item, "Batch", f"1 / {batch_throw}")
                                        data_tree.set(item, "Status", "Done")
                                        data_tree.set(item, "Total Successful Toggles", total_successful_toggles)  # Update total successful toggles
                                        break

                            # Enable download button
                            download_button.config(state="normal")
                            download_button['command'] = lambda: download_data(tagged_conversations)
                            
                        #Time Out Error
                        elif tag_order_id == "error" and tag_id_to_add == "time_out":
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Tree
                            items2 = data_tree.get_children()
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                                    data_tree.set(item2, "Status", "Time Out")
                                    data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                    break
                                
                        else:
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'

                            running_data_text.insert(tk.END, f"Error: No tag with the name '{tag_id_name}' found.\n")
                            running_data_text.yview(tk.END)
                            
                            #Update Data Tree 
                            items2 = data_tree.get_children()
                            print("exe", page_id,access_token,tag_id_name ,input_start_date,input_end_date,start_time, end_time,input_start_schedule_date ,scheduled_time )
                        
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                print("table", values2[0] ,values2[1],values2[4], values2[5], values2[6], values2[7],values2[8] ,values2[9],values2[10])
                        
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                               
                                    data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                                    data_tree.set(item2, "Status", "Failed")
                                    data_tree.set(item2, "Total Successful Toggles", "No Tag Name")
                                    break
                            
                    #2ND Throw
                    elif throw == 2 and on_batch2 == 1:
                        running_data_text.delete('1.0', tk.END)
                       
                        # Get the date from 10 days ago up to yesterday(AM)
                        start_date = (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d")
                        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                        start_hour = "00"
                        start_minute = "00"
                        start_seconds = "00"
                        end_hour = "23"
                        end_minute = "59"
                        end_seconds = "59"
                        
                        print("2nd Throw :", start_date, end_date)
                        start_datetime = datetime.strptime(f"{start_date} {start_hour}:{start_minute}:{start_seconds}", "%Y-%m-%d %H:%M:%S")
                        start_time = int(start_datetime.timestamp())

                        # Combine end date, hour, minute, and second (with conversational Time)
                        end_datetime = datetime.strptime(f"{end_date} {end_hour}:{end_minute}:{end_seconds}", "%Y-%m-%d %H:%M:%S")
                        end_time = int(end_datetime.timestamp())
                        

                        # API URL to retrieve tag info
                        tag_info_api_url = f"https://pancake.ph/api/v1/pages/{page_id}/settings?access_token={access_token}"

                        # Get the tag_order_id and tag_id_to_add
                        tag_order_id, tag_id_to_add = get_tag_info(tag_id_name, tag_info_api_url)

                        if tag_order_id is not None and tag_id_to_add is not None:
                            # Construct URL with epoch time and tag_order_id (end time edited)
                            initial_url = f"https://pancake.ph/api/v1/pages/{page_id}/conversations?type=NOPHONE,INBOX,CREATE_DATE:{start_time}+-+{end_time}&mode=OR&tags=[]&except_tags=[{tag_order_id}]&access_token={access_token}&from_platform=web"
                            

                            # List to store tagged conversations
                            tagged_conversations = []
                            unique_conversation_id = []
                            # Variable to Store Toral Successful toggles
                            total_successful_toggles = 0
                            
                            # Loop through the process for the specified number of iterations
                            for iteration in range(num_iterations):
                                
                                # Initialize progress bar
                                progress_bar["value"] = iteration
                                progress_bar["maximum"] = num_iterations
                                progress_bar_label.config(text=f"Progress: {iteration+1}%")
                                
                                #Update Data Tree as Ongoing
                                start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                items3 = data_tree.get_children()
                                for item3 in items3:
                                    
                                    values3 = data_tree.item(item3, 'values')
                                    if values3 and values3[0] == page_id and values3[1] == access_token and values3[4] == tag_id_name and values3[5] == input_start_date and values3[6] == input_end_date and values3[7] == start_time and values3[8] == end_time and values3[9] == input_start_schedule_date and values3[10] == scheduled_time:
                                        data_tree.set(item3, "Batch", f"2 / {batch_throw}")
                                        data_tree.set(item3, "Status", "Ongoing")  # Update total ongoing toggles
                                        break
                                
                                try:
                                    response = requests.get(initial_url)
                                    data = response.json()
                                except requests.exceptions.JSONDecodeError:
                                    try:
                                        response = requests.get(initial_url)
                                        data = response.json()
                                    except requests.exceptions.JSONDecodeError:
                                        start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                        end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                        
                                        scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                        
                                        #Update Data Tree
                                        items2 = data_tree.get_children()
                                        for item2 in items2:
                                            values2 = data_tree.item(item2, 'values')
                                            if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                                data_tree.set(item2, "Batch", f"2 / {batch_throw}")
                                                data_tree.set(item2, "Status", "Time Out")
                                                data_tree.set(item2, "Total Successful Toggles", total_success_tag + total_success_tag)
                                                break
                                        messagebox.showerror("Error", "Invalid Response/Time Out")
                                except requests.exceptions.RequestException as e:
                                    # Handle other request exceptions
                                    try: 
                                        response = requests.get(initial_url)
                                        data = response.json()
                                    except requests.exceptions.RequestException as e:
                                        start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                        end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                        
                                        scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                        
                                        #Update Data Tree
                                        items2 = data_tree.get_children()
                                        for item2 in items2:
                                            values2 = data_tree.item(item2, 'values')
                                            if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                                data_tree.set(item2, "Batch", f"2 / {batch_throw}")
                                                data_tree.set(item2, "Status", "Lost Connection")
                                                data_tree.set(item2, "Total Successful Toggles", total_success_tag + total_success_tag)
                                                break
                                        message = f"Request failed: {e}"
                                        messagebox.showerror("Error", message)

                                # Extract the conversations from the initial response
                                conversations = data.get("conversations", [])

                                # Process each conversation to toggle tag using threading
                                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                                    results = executor.map(toggle_tag_for_from_id, [(conv.get("from", {}).get("id"), page_id, access_token, tag_id_to_add, running_data_text, progress_bar) for conv in conversations])
                                    for success, conv_id in zip(results, [conv.get("from", {}).get("id") for conv in conversations]):
                                        # progress_bar["value"] += 1 # Increment total successful toggles
                                        root.update_idletasks()  # Update GUI
                                        if success:
                                            if conv_id not in unique_conversation_id:
                                                total_successful_toggles += 1
                                                tagged_conversations.append(conv_id)
                                                unique_conversation_id.append(conv_id)
                                            else:
                                                print("Already mention")

                            # Update running data text
                            running_data_text.insert(tk.END, f"2nd Throw Total successful tag toggles: {total_successful_toggles}\n")
                            running_data_text.yview(tk.END)
                            root.bell()
                            # global unique_conv_id
                            unique_conv_id = []
                            toggle_tag_for_from_id.counter = 1
                            
                            #Filter Start and End Time for Update of Table
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"

                            # Update the status in data_tree to "Done"
                            for conv_id in tagged_conversations:
                                # Find the item in the treeview with matching conversation ID
                                items = data_tree.get_children()
                                for item in items:
                                    values = data_tree.item(item, 'values')
                                    if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                        data_tree.set(item, "Batch", f"2 / {batch_throw}")
                                        data_tree.set(item, "Status", "Done")
                                        data_tree.set(item, "Total Successful Toggles", total_successful_toggles + total_success_tag)  # Update total successful toggles
                                        break
                            
                            #Update Data tree has no conversations
                            if total_successful_toggles == 0:
                                items = data_tree.get_children()
                                for item in items:
                                    values = data_tree.item(item, 'values')
                                    if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time  and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                        data_tree.set(item, "Batch", f"2 / {batch_throw}")
                                        data_tree.set(item, "Status", "Done")
                                        data_tree.set(item, "Total Successful Toggles", total_successful_toggles + total_success_tag)  # Update total successful toggles
                                        break

                            # Enable download button
                            download_button.config(state="normal")
                            download_button['command'] = lambda: download_data(tagged_conversations)
                            
                        #Time Out Error
                        elif tag_order_id == "error" and tag_id_to_add == "time_out":
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Tree
                            items2 = data_tree.get_children()
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Batch", f"2 / {batch_throw}")
                                    data_tree.set(item2, "Status", "Time Out")
                                    data_tree.set(item2, "Total Successful Toggles", total_success_tag + total_success_tag)
                                    break
                                
                        else:
                            
                            running_data_text.insert(tk.END, f"Error: No tag with the name '{tag_id_name}' found.\n")
                            running_data_text.yview(tk.END)
                            
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Three
                            items2 = data_tree.get_children()
                            print("exe", page_id,access_token,tag_id_name ,input_start_date,input_end_date,start_time, end_time,input_start_schedule_date ,scheduled_time )
                        
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                print("table", values2[0] ,values2[1],values2[4], values2[5], values2[6], values2[7],values2[8] ,values2[9],values2[10])
                        
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Batch", f"2 / {batch_throw}")
                                    data_tree.set(item2, "Status", "Failed")
                                    if total_success_tag == 0:
                                        data_tree.set(item2, "Total Successful Toggles", "No Tag Name")
                                    else:
                                        data_tree.set(item2, "Total Successful Toggles", "No Tag Name : Success: "+ total_success_tag)
                                    break
                            
                    #3RD Throw
                    elif throw == 3 and on_batch3 == 1:
                        running_data_text.delete('1.0', tk.END)
         
                        # Get the date from 30 days ago up to yesterday(AM)
                        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                        end_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                        start_hour = "00"
                        start_minute = "00"
                        start_seconds = "00"
                        end_hour = "23"
                        end_minute = "59"
                        end_seconds = "59"
   
                        
                        print("3rd Throw :", start_date, end_date)
                        start_datetime = datetime.strptime(f"{start_date} {start_hour}:{start_minute}:{start_seconds}", "%Y-%m-%d %H:%M:%S")
                        start_time = int(start_datetime.timestamp())

                        # Combine end date, hour, minute, and second (with conversational Time)
                        end_datetime = datetime.strptime(f"{end_date} {end_hour}:{end_minute}:{end_seconds}", "%Y-%m-%d %H:%M:%S")
                        end_time = int(end_datetime.timestamp())
                        

                        # API URL to retrieve tag info
                        tag_info_api_url = f"https://pancake.ph/api/v1/pages/{page_id}/settings?access_token={access_token}"

                        # Get the tag_order_id and tag_id_to_add
                        tag_order_id, tag_id_to_add = get_tag_info(tag_id_name, tag_info_api_url)

                        if tag_order_id is not None and tag_id_to_add is not None:
                            # Construct URL with epoch time and tag_order_id (end time edited)
                            initial_url = f"https://pancake.ph/api/v1/pages/{page_id}/conversations?type=NOPHONE,INBOX,CREATE_DATE:{start_time}+-+{end_time}&mode=OR&tags=[]&except_tags=[{tag_order_id}]&access_token={access_token}&from_platform=web"

                            # List to store tagged conversations
                            tagged_conversations = []
                            unique_conversation_id = []
                            # Variable to Store Toral Successful toggles
                            total_successful_toggles = 0
                            
                            # Loop through the process for the specified number of iterations
                            for iteration in range(num_iterations):
                                
                                # Initialize progress bar
                                progress_bar["value"] = iteration
                                progress_bar["maximum"] = num_iterations
                                progress_bar_label.config(text=f"Progress: {iteration+1}%")
                                
                                #Update Data Tree as Ongoing
                                start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                items3 = data_tree.get_children()
                                for item3 in items3:
                                    values3 = data_tree.item(item3, 'values')
                                    if values3 and values3[0] == page_id and values3[1] == access_token and values3[4] == tag_id_name and values3[5] == input_start_date and values3[6] == input_end_date and values3[7] == start_time and values3[8] == end_time and values3[9] == input_start_schedule_date and values3[10] == scheduled_time:
                                        data_tree.set(item3, "Batch", f"3 / {batch_throw}")
                                        data_tree.set(item3, "Status", "Ongoing")  # Update total ongoing toggles
                                        break
                                
                                try:
                                    response = requests.get(initial_url)
                                    data = response.json()
                                    
                                except requests.exceptions.JSONDecodeError:
                                    try:
                                        response = requests.get(initial_url)
                                        data = response.json()
                                    except requests.exceptions.JSONDecodeError:
                                        start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                        end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                        
                                        scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                        
                                        #Update Data Tree
                                        items2 = data_tree.get_children()
                                        for item2 in items2:
                                            values2 = data_tree.item(item2, 'values')
                                            if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                                data_tree.set(item2, "Batch", f"3 / {batch_throw}")
                                                data_tree.set(item2, "Status", "Time Out")
                                                data_tree.set(item2, "Total Successful Toggles", total_success_tag + total_success_tag)
                                                break
                                        messagebox.showerror("Error", "Invalid Response/Time Out")

                                except requests.exceptions.RequestException as e:
                                    # Handle other request exceptions
                                    try:
                                        response = requests.get(initial_url)
                                        data = response.json()
                                    except requests.exceptions.RequestException as e:
                                        start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                        end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                        
                                        scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                        
                                        #Update Data Tree
                                        items2 = data_tree.get_children()
                                        for item2 in items2:
                                            values2 = data_tree.item(item2, 'values')
                                            if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                                data_tree.set(item2, "Batch", f"3 / {batch_throw}")
                                                data_tree.set(item2, "Status", "Lost Connection")
                                                data_tree.set(item2, "Total Successful Toggles", total_success_tag + total_success_tag)
                                                break
                                        message = f"Request failed: {e}"
                                        messagebox.showerror("Error", message)

                                # Extract the conversations from the initial response
                                conversations = data.get("conversations", [])

                                # Process each conversation to toggle tag using threading
                                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                                    results = executor.map(toggle_tag_for_from_id, [(conv.get("from", {}).get("id"), page_id, access_token, tag_id_to_add, running_data_text, progress_bar) for conv in conversations])
                                    for success, conv_id in zip(results, [conv.get("from", {}).get("id") for conv in conversations]):
                                        # progress_bar["value"] += 1 # Increment total successful toggles
                                        root.update_idletasks()  # Update GUI
                                        if success:
                                            if conv_id not in unique_conversation_id:
                                                total_successful_toggles += 1
                                                tagged_conversations.append(conv_id)
                                                unique_conversation_id.append(conv_id)
                                            else:
                                                print("Already mention")

                            # Update running data text
                            running_data_text.insert(tk.END, f"3rd Throw Total successful tag toggles: {total_successful_toggles}\n")
                            running_data_text.yview(tk.END)
                            root.bell()
                            # global unique_conv_id
                            unique_conv_id = []
                            toggle_tag_for_from_id.counter = 1
                            
                            #Filter Start and End Time for Update of Table
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            # Update the status in data_tree to "Done"
                            for conv_id in tagged_conversations:
                                # Find the item in the treeview with matching conversation ID
                                items = data_tree.get_children()
                                for item in items:
                                    values = data_tree.item(item, 'values')
                                    if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                        data_tree.set(item, "Batch", f"3 / {batch_throw}")
                                        data_tree.set(item, "Status", "Done")
                                        data_tree.set(item, "Total Successful Toggles", total_successful_toggles + total_success_tag)  # Update total successful toggles
                                        break
                                    
                            if total_successful_toggles == 0:
                                items = data_tree.get_children()
                                for item in items:
                                    values = data_tree.item(item, 'values')
                                    if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                        data_tree.set(item, "Batch", f"3 / {batch_throw}")
                                        data_tree.set(item, "Status", "Done")
                                        data_tree.set(item, "Total Successful Toggles", total_successful_toggles + total_success_tag)  # Update total successful toggles
                                        break

                            # Enable download button
                            download_button.config(state="normal")
                            download_button['command'] = lambda: download_data(tagged_conversations)
                        
                        #Time Out Error
                        elif tag_order_id == "error" and tag_id_to_add == "time_out":
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Tree
                            items2 = data_tree.get_children()
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Batch", f"3 / {batch_throw}")
                                    data_tree.set(item2, "Status", "Time Out")
                                    data_tree.set(item2, "Total Successful Toggles", total_success_tag + total_success_tag)
                                    break
                        
                        else:
                            start_time = f'{start_hour}:{start_minute} {start_seconds}'
                            end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                            running_data_text.insert(tk.END, f"Error: No tag with the name '{tag_id_name}' found.\n")
                            running_data_text.yview(tk.END)
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Tree
                            items2 = data_tree.get_children()
                            print("exe", page_id,access_token,tag_id_name ,input_start_date,input_end_date,start_time, end_time,input_start_schedule_date ,scheduled_time )
                        
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                print("table", values2[0] ,values2[1],values2[4], values2[5], values2[6], values2[7],values2[8] ,values2[9],values2[10])
                        
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Batch", f"3 / {batch_throw}")
                                    data_tree.set(item2, "Status", "Failed")
                                    if total_success_tag == 0:
                                        data_tree.set(item2, "Total Successful Toggles", "No Tag Name")
                                    else:
                                        data_tree.set(item2, "Total Successful Toggles", "No Tag Name", ":","Success:", total_success_tag)
                                    break
            else:
                # PM Shift
                # Get the date Today and Time
                start_date = datetime.now().strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_hour = "00"
                start_minute = "00"
                start_seconds = "00"
                end_hour = "23"
                end_minute = "59"
                end_seconds = "59"
                        
                start_datetime = datetime.strptime(f"{start_date} {start_hour}:{start_minute}:{start_seconds}", "%Y-%m-%d %H:%M:%S")
                start_time = int(start_datetime.timestamp())

                # Combine end date, hour, minute, and second (with conversational Time)
                end_datetime = datetime.strptime(f"{end_date} {end_hour}:{end_minute}:{end_seconds}", "%Y-%m-%d %H:%M:%S")
                end_time = int(end_datetime.timestamp())
                        

                # API URL to retrieve tag info
                tag_info_api_url = f"https://pancake.ph/api/v1/pages/{page_id}/settings?access_token={access_token}"

                # Get the tag_order_id and tag_id_to_add
                tag_order_id, tag_id_to_add = get_tag_info(tag_id_name, tag_info_api_url)

                if tag_order_id is not None and tag_id_to_add is not None:
                    # Construct URL with epoch time and tag_order_id (end time edited)
                    initial_url = f"https://pancake.ph/api/v1/pages/{page_id}/conversations?type=NOPHONE,INBOX,CREATE_DATE:{start_time}+-+{end_time}&mode=OR&tags=[]&except_tags=[{tag_order_id}]&access_token={access_token}&from_platform=web"

                    # List to store tagged conversations
                    tagged_conversations = []
                    unique_conversation_id = []
                    # Variable to Store Toral Successful toggles
                    total_successful_toggles = 0
                    
                    # Loop through the process for the specified number of iterations
                    for iteration in range(num_iterations):

                        # Initialize progress bar
                        progress_bar["value"] = iteration
                        progress_bar["maximum"] = num_iterations
                        progress_bar_label.config(text=f"Progress: {iteration+1}%")
                                
                        #Update Data Tree as Ongoing
                        start_time = f'{start_hour}:{start_minute} {start_seconds}'
                        end_time = f'{end_hour}:{end_minute} {end_seconds}'
                        scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                        items3 = data_tree.get_children()
                        for item3 in items3:
                            values3 = data_tree.item(item3, 'values')
                            if values3 and values3[0] == page_id and values3[1] == access_token and values3[4] == tag_id_name and values3[5] == input_start_date and values3[6] == input_end_date and values3[7] == start_time and values3[8] == end_time and values3[9] == input_start_schedule_date and values3[10] == scheduled_time:
                                data_tree.set(item3, "Batch", f"{batch_throw} / {batch_throw}")
                                data_tree.set(item3, "Status", "Ongoing")  # Update total ongoing toggles
                                break
                                
                        try:
                            response = requests.get(initial_url)
                            data = response.json()
                        except requests.exceptions.JSONDecodeError:
                            try:
                                response = requests.get(initial_url)
                                data = response.json()
                            except requests.exceptions.JSONDecodeError:
                                start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                
                                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                
                                #Update Data Tree
                                items2 = data_tree.get_children()
                                for item2 in items2:
                                    values2 = data_tree.item(item2, 'values')
                                    if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                        data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                                        data_tree.set(item2, "Status", "Time Out")
                                        data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                        break
                                messagebox.showerror("Error", "Invalid Response/Time Out")
                        except requests.exceptions.RequestException as e:
                            # Handle other request exceptions
                            try: 
                                response = requests.get(initial_url)
                                data = response.json()
                            except requests.exceptions.RequestException as e:
                                start_time = f'{start_hour}:{start_minute} {start_seconds}'
                                end_time = f'{end_hour}:{end_minute} {end_seconds}'
                                
                                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                                
                                #Update Data Tree
                                items2 = data_tree.get_children()
                                for item2 in items2:
                                    values2 = data_tree.item(item2, 'values')
                                    if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                        data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                                        data_tree.set(item2, "Status", "Lost Connection")
                                        data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                        break

                                message = f"Request failed: {e}"
                                messagebox.showerror("Error", message)

                        # Extract the conversations from the initial response
                        conversations = data.get("conversations", [])

                        # Process each conversation to toggle tag using threading
                        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                            results = executor.map(toggle_tag_for_from_id, [(conv.get("from", {}).get("id"), page_id, access_token, tag_id_to_add, running_data_text, progress_bar) for conv in conversations])
                            for success, conv_id in zip(results, [conv.get("from", {}).get("id") for conv in conversations]):
                                # progress_bar["value"] += 1 # Increment total successful toggles
                                root.update_idletasks()  # Update GUI
                                if success:
                                    if conv_id not in unique_conversation_id:
                                        total_successful_toggles += 1
                                        tagged_conversations.append(conv_id)
                                        unique_conversation_id.append(conv_id)
                                    else:
                                        print("Already mention")

                    # Update running data text
                    running_data_text.insert(tk.END, f"Total successful tag toggles: {total_successful_toggles}\n")
                    running_data_text.yview(tk.END)
                    root.bell()
                    # global unique_conv_id
                    total_success_tag = total_successful_toggles
                    unique_conv_id = []
                    toggle_tag_for_from_id.counter = 1
                    
                    #Filter Start and End Time for Update of Table
                    start_time = f'{start_hour}:{start_minute} {start_seconds}'
                    end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"

                    # Update the status in data_tree to "Done"
                    for conv_id in tagged_conversations:
                        # Find the item in the treeview with matching conversation ID
                        items = data_tree.get_children()
                        for item in items:
                                    
                            values = data_tree.item(item, 'values')
                            if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                data_tree.set(item, "Batch", f"{batch_throw}/ {batch_throw}")
                                data_tree.set(item, "Status", "Done")
                                data_tree.set(item, "Total Successful Toggles", total_successful_toggles)  # Update total successful toggles
                                break
                            
                    #Update Data Tree
                    if total_successful_toggles == 0:
                        items = data_tree.get_children()
                        for item in items:
                            values = data_tree.item(item, 'values')
                            if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                                data_tree.set(item, "Batch", f"{batch_throw} / {batch_throw}")
                                data_tree.set(item, "Status", "Done")
                                data_tree.set(item, "Total Successful Toggles", total_successful_toggles)  # Update total successful toggles
                                break

                    # Enable download button
                    download_button.config(state="normal")
                    download_button['command'] = lambda: download_data(tagged_conversations)
                            
                #Time Out Error
                elif tag_order_id == "error" and tag_id_to_add == "time_out":
                    start_time = f'{start_hour}:{start_minute} {start_seconds}'
                    end_time = f'{end_hour}:{end_minute} {end_seconds}'
                    
                    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                    
                    #Update Data Tree
                    items2 = data_tree.get_children()
                    for item2 in items2:
                        values2 = data_tree.item(item2, 'values')
                        if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                            data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                            data_tree.set(item2, "Status", "Time Out")
                            data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                            break
                                
                else:
                    start_time = f'{start_hour}:{start_minute} {start_seconds}'
                    end_time = f'{end_hour}:{end_minute} {end_seconds}'
                            
                    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                    
                    running_data_text.insert(tk.END, f"Error: No tag with the name '{tag_id_name}' found.\n")
                    running_data_text.yview(tk.END)
                    
                    #Update Data Tree 
                    items2 = data_tree.get_children()
                    print("exe", page_id,access_token,tag_id_name ,input_start_date,input_end_date,start_time, end_time,input_start_schedule_date ,scheduled_time )
                    for item2 in items2:
                        values2 = data_tree.item(item2, 'values')
                        print("table", values2[0] ,values2[1],values2[4], values2[5], values2[6], values2[7],values2[8] ,values2[9],values2[10])
                        
                        if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                            data_tree.set(item2, "Batch", f"1 / {batch_throw}")
                            data_tree.set(item2, "Status", "Failed")
                            data_tree.set(item2, "Total Successful Toggles", "No Tag Name")
                            break

                    
        else:
            #Custom Throw (Throw Tags based on the customed datetime conversation datetime range)
            # Combine start date, hour, minute, and second(with conversational Time)
            start_datetime = datetime.strptime(f"{input_start_date} {input_start_hour}:{input_start_minute}:{input_start_second}", "%Y-%m-%d %H:%M:%S")
            start_time = int(start_datetime.timestamp())

            # Combine end date, hour, minute, and second (with conversational Time)
            end_datetime = datetime.strptime(f"{input_end_date} {input_end_hour}:{input_end_minute}:{input_end_second}", "%Y-%m-%d %H:%M:%S")
            end_time = int(end_datetime.timestamp())
            

            # API URL to retrieve tag info
            tag_info_api_url = f"https://pancake.ph/api/v1/pages/{page_id}/settings?access_token={access_token}"

            # Get the tag_order_id and tag_id_to_add
            tag_order_id, tag_id_to_add = get_tag_info(tag_id_name, tag_info_api_url)

            if tag_order_id is not None and tag_id_to_add is not None:
                # Construct URL with epoch time and tag_order_id (end time edited)
                initial_url = f"https://pancake.ph/api/v1/pages/{page_id}/conversations?type=NOPHONE,INBOX,CREATE_DATE:{start_time}+-+{end_time}&mode=OR&tags=[]&except_tags=[{tag_order_id}]&access_token={access_token}&from_platform=web"

                # List to store tagged conversations
                tagged_conversations = []
                unique_conversation_id = []
                # Variable to Store Toral Successful toggles
                total_successful_toggles = 0
                
                # Loop through the process for the specified number of iterations
                for iteration in range(num_iterations):
                    
                    # Initialize progress bar
                    progress_bar["value"] = iteration
                    progress_bar["maximum"] = num_iterations
                    progress_bar_label.config(text=f"Progress: {iteration+1}%")
                    
                    #Update Data Tree as Ongoing
                    start_time = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                    end_time = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                    items3 = data_tree.get_children()
                    for item3 in items3:
                        values3 = data_tree.item(item3, 'values')
                        if values3 and values3[0] == page_id and values3[1] == access_token and values3[4] == tag_id_name and values3[5] == input_start_date and values3[6] == input_end_date and values3[7] == start_time and values3[8] == end_time and values3[9] == input_start_schedule_date and values3[10] == scheduled_time:
                            data_tree.set(item3, "Status", "Ongoing")  # Update total ongoing toggles
                            break
                    
                    try:
                        response = requests.get(initial_url)
                        data = response.json()
                    except requests.exceptions.JSONDecodeError:
                        try:
                            response = requests.get(initial_url)
                            data = response.json()
                        except requests.exceptions.JSONDecodeError:
                            start_time = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                            end_time = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Tree
                            items2 = data_tree.get_children()
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Status", "Time Out")
                                    data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                    break
                            messagebox.showerror("Error", "Invalid Response/Time Out")
                    except requests.exceptions.RequestException as e:
                        # Handle other request exceptions
                        try:
                            response = requests.get(initial_url)
                            data = response.json()
                        except requests.exceptions.RequestException as e:
                            start_time = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                            end_time = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                            
                            scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                            
                            #Update Data Tree
                            items2 = data_tree.get_children()
                            for item2 in items2:
                                values2 = data_tree.item(item2, 'values')
                                if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                                    data_tree.set(item2, "Status", "Lost Connection")
                                    data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                                    break
                            message = f"Request failed: {e}"
                            messagebox.showerror("Error", message)
                 

                    # Extract the conversations from the initial response
                    conversations = data.get("conversations", [])

                    # Process each conversation to toggle tag using threading
                    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                        results = executor.map(toggle_tag_for_from_id, [(conv.get("from", {}).get("id"), page_id, access_token, tag_id_to_add, running_data_text, progress_bar) for conv in conversations])
                        for success, conv_id in zip(results, [conv.get("from", {}).get("id") for conv in conversations]):
                            # progress_bar["value"] += 1 # Increment total successful toggles
                            root.update_idletasks()  # Update GUI
                            if success:
                                if conv_id not in unique_conversation_id:
                                    total_successful_toggles += 1
                                    tagged_conversations.append(conv_id)
                                    unique_conversation_id.append(conv_id)
                                else:
                                    print("Already mention")

                # Update running data text
                running_data_text.insert(tk.END, f"Total successful tag toggles: {total_successful_toggles}\n")
                running_data_text.yview(tk.END)
                root.bell()
                # global unique_conv_id
                unique_conv_id = []
                toggle_tag_for_from_id.counter = 1
                
                #Filter Start and End Time for Update of Table
                start_time = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                end_time = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                
                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                
                # Update the status in data_tree to "Done"
                for conv_id in tagged_conversations:
                    # Find the item in the treeview with matching conversation ID
                    items = data_tree.get_children()
                    for item in items:
                        values = data_tree.item(item, 'values')
                        if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                            data_tree.set(item, "Status", "Done")
                            data_tree.set(item, "Total Successful Toggles", total_successful_toggles)  # Update total successful toggles
                            break
                
                #No successful Tags/No Tags
                if total_successful_toggles == 0:
                    items = data_tree.get_children()
                    for item in items:
                        values = data_tree.item(item, 'values')
                        if values and values[0] == page_id and values[1] == access_token and values[4] == tag_id_name and values[5] == input_start_date and values[6] == input_end_date and values[7] == start_time and values[8] == end_time and values[9] == input_start_schedule_date and values[10] == scheduled_time:
                            data_tree.set(item, "Status", "Done")
                            data_tree.set(item, "Total Successful Toggles", total_successful_toggles)  # Update total successful toggles
                            break

                # Enable download button
                download_button.config(state="normal")
                download_button['command'] = lambda: download_data(tagged_conversations)
            
            #Time Out Error
            elif tag_order_id == "error" and tag_id_to_add == "time_out":
                start_time = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                end_time = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                
                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                
                #Update Data Tree
                items2 = data_tree.get_children()
                for item2 in items2:
                    values2 = data_tree.item(item2, 'values')
                    if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                        data_tree.set(item2, "Status", "Time Out")
                        data_tree.set(item2, "Total Successful Toggles", total_success_tag)
                        break
            else:
                
                running_data_text.insert(tk.END, f"Error: No tag with the name '{tag_id_name}' found.\n")
                running_data_text.yview(tk.END)
                
                start_time = f'{input_start_hour}:{input_start_minute} {input_start_second}'
                end_time = f'{input_end_hour}:{input_end_minute} {input_end_second}'
                
                scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
                
                #Update Data Tree
                items2 = data_tree.get_children()
                print("exe", page_id,access_token,tag_id_name ,input_start_date,input_end_date,start_time, end_time,input_start_schedule_date ,scheduled_time )
                for item2 in items2:
                    values2 = data_tree.item(item2, 'values')
                    print("table", values2[0] ,values2[1],values2[4], values2[5], values2[6], values2[7],values2[8] ,values2[9],values2[10])
                    if values2 and values2[0] == page_id and values2[1] == access_token and values2[4] == tag_id_name and values2[5] == input_start_date and values2[6] == input_end_date and values2[7] == start_time and values2[8] == end_time and values2[9] == input_start_schedule_date and values2[10] == scheduled_time:
                        data_tree.set(item2, "Status", "Failed")
                        data_tree.set(item2, "Total Successful Toggles", "No Tag Name")
                        break
                    
    elif datetime.now() > check_end_schedule_date:
        schedule.clear('execute_task')

    # return page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, input_start_hour, input_start_minute, input_start_second, input_end_hour, input_end_minute, input_end_second, shift, batch_throw, input_start_schedule_date, input_schedule_hour, input_schedule_minute, input_schedule_ampm, input_end_schedule_date, scheduled_pattern, on_batch1, on_batch2, on_batch3
    # Re-enable submit button after execution
    submit_button.config(state="normal")

# Function to update the table with the form data
def update_table(batch):
    # Get the current time
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    #Get Conversation Start and End DateTime
    start_date , end_date , start_hour, start_minute, start_seconds, end_hour, end_minute, end_seconds, shift, batch_throw, changed_schedule_hour, changed_schedule_minute, changed_schedule_ampm,changed_schedule_hour2, changed_schedule_minute2, changed_schedule_ampm2, changed_schedule_hour3, changed_schedule_minute3, changed_schedule_ampm3, on_batch1, on_batch2, on_batch3 = toggle_batch_throw()
    
    input_start_schedule_date = input_start_schedule_date_entry.get()
    # Check if PM Change Default schduled Time
    if shift == 0 and batch == "1":
        throw = 1
        display_throw = 1
        if changed_schedule_hour != "05" or changed_schedule_minute != "00" or changed_schedule_ampm != "PM":
            schedule_hour = changed_schedule_hour
            schedule_minute = changed_schedule_minute
            schedule_ampm = changed_schedule_ampm
            input_schedule_hour_var.set(schedule_hour)
            input_schedule_minute_var.set(schedule_minute)
            input_schedule_ampm_var.set(schedule_ampm)

            input_schedule_hour = input_schedule_hour_combobox.get()
            input_schedule_minute = input_schedule_minute_combobox.get()
            input_schedule_ampm = input_schedule_ampm_combobox.get()
        else:
            input_schedule_hour = input_schedule_hour_combobox.get()
            input_schedule_minute = input_schedule_minute_combobox.get()
            input_schedule_ampm = input_schedule_ampm_combobox.get()
        status = "Scheduled"
    elif shift == 0 and batch == "2":
        throw = 2
        display_throw = 2
        if changed_schedule_hour2 != "08" or changed_schedule_minute2 != "00" or changed_schedule_ampm2 != "PM":
            schedule_hour = changed_schedule_hour2
            schedule_minute = changed_schedule_minute2
            schedule_ampm = changed_schedule_ampm2
            input_schedule_hour_var2.set(schedule_hour)
            input_schedule_minute_var2.set(schedule_minute)
            input_schedule_ampm_var2.set(schedule_ampm)
            input_schedule_hour = input_schedule_hour_combobox2.get()
            input_schedule_minute = input_schedule_minute_combobox2.get()
            input_schedule_ampm = input_schedule_ampm_combobox2.get()
        else:
            input_schedule_hour = input_schedule_hour_combobox2.get()
            input_schedule_minute = input_schedule_minute_combobox2.get()
            input_schedule_ampm = input_schedule_ampm_combobox2.get()
        status = "Scheduled"
    elif shift == 0 and batch == "3":
        throw = 3
        display_throw = 3
        if changed_schedule_hour3 != "12" or changed_schedule_minute3 != "00" or changed_schedule_ampm3 != "AM":
            schedule_hour = changed_schedule_hour3
            schedule_minute = changed_schedule_minute3
            schedule_ampm = changed_schedule_ampm3
            input_schedule_hour_var3.set(schedule_hour)
            input_schedule_minute_var3.set(schedule_minute)
            input_schedule_ampm_var3.set(schedule_ampm)
            input_schedule_hour = input_schedule_hour_combobox3.get()
            input_schedule_minute = input_schedule_minute_combobox3.get()
            input_schedule_ampm = input_schedule_ampm_combobox3.get()
        else:
            today = datetime.now().date()
            # Calculate tomorrow's date
            tomorrow = today + timedelta(days=1)
            # Format tomorrow's date as month/day/year
            formatted_date = tomorrow.strftime("%m/%d/%y").lstrip("0")
            input_start_schedule_date = formatted_date

            input_schedule_hour = input_schedule_hour_combobox3.get()
            input_schedule_minute = input_schedule_minute_combobox3.get()
            input_schedule_ampm = input_schedule_ampm_combobox3.get()
        status = "Scheduled"

    elif shift==1:
        input_schedule_hour = input_schedule_hour_combobox.get()
        input_schedule_minute = input_schedule_minute_combobox.get()
        input_schedule_ampm = input_schedule_ampm_combobox.get()

        if on_batch1 == 1 and on_batch2 == 0 and on_batch3 == 0:
            display_throw = 1
        elif on_batch1 == 0 and on_batch2 == 1 and on_batch3 == 0:
            display_throw = 2
        elif on_batch1 == 0 and on_batch2 == 0 and on_batch3 == 1:
            display_throw = 3
        elif on_batch1 == 1 and on_batch2 == 1 and on_batch3 == 0:
            display_throw = "1, 2"
        elif on_batch1 == 1 and on_batch2 == 0 and on_batch3 == 1:
            display_throw = "1, 3"
        elif on_batch1 == 0 and on_batch2 == 1 and on_batch3 == 1:
            display_throw = "2, 3"
        elif on_batch1 == 1 and on_batch2 == 1 and on_batch3 == 1:
            display_throw = "1, 2, 3"
        else:
            display_throw = "Custom"

        status = "Scheduled"
    else:
        input_schedule_hour = input_schedule_hour_combobox.get()
        input_schedule_minute = input_schedule_minute_combobox.get()
        input_schedule_ampm = input_schedule_ampm_combobox.get()

        display_throw = "Custom"
        status = "Scheduled"
        
    if auto_run_var.get() == 1:

        current_time = datetime.now()

        # Extract hour, minute, and AM/PM
        input_schedule_hour = current_time.strftime("%I")  # %I for 12-hour format, %H for 24-hour format
        input_schedule_minute = current_time.strftime("%M")
        input_schedule_ampm = current_time.strftime("%p")

        if on_batch1 == 1 and on_batch2 == 0 and on_batch3 == 0:
            display_throw = 1
        elif on_batch1 == 0 and on_batch2 == 1 and on_batch3 == 0:
            display_throw = 2
        elif on_batch1 == 0 and on_batch2 == 0 and on_batch3 == 1:
            display_throw = 3
        elif on_batch1 == 1 and on_batch2 == 1 and on_batch3 == 0:
            display_throw = "1, 2"
        elif on_batch1 == 1 and on_batch2 == 0 and on_batch3 == 1:
            display_throw = "1, 3"
        elif on_batch1 == 0 and on_batch2 == 1 and on_batch3 == 1:
            display_throw = "2, 3"
        elif on_batch1 == 1 and on_batch2 == 1 and on_batch3 == 1:
            display_throw = "1, 2, 3"
        else:
            display_throw = "Custom"

        status = "Immediate Run"
        
    
    # Get the form input values
    page_id = page_id_entry.get()
    access_token = access_token_entry.get()
    num_iterations = num_iterations_entry.get()
    max_workers = max_workers_entry.get()
    tag_id_name = tag_id_to_add_entry.get()
    input_start_date = start_date
    input_end_date = end_date
    
    #conversational time
    input_start_hour = start_hour
    input_start_minute = start_minute
    input_start_second = start_seconds
    input_end_hour = end_hour
    input_end_minute = end_minute
    input_end_second = end_seconds
    #------------
    
    # Combine scheduled date and time into a single string
    scheduled_time = f"{input_schedule_hour}:{input_schedule_minute} {input_schedule_ampm}"
    
    #Conversational Format
    start_time = f"{input_start_hour}:{input_start_minute} {input_start_second}"
    end_time = f"{input_end_hour}:{input_end_minute} {input_end_second}"
    schedule_pattern = input_schedule_pattern_combobox.get()
    weekly_pattern = input_weekly_pattern_combobox.get()

    if auto_run_var.get() == 1:
        pattern = "Immediately Run"
    elif schedule_pattern == "Weekly":
        pattern = f"{schedule_pattern}:{weekly_pattern}"
    else:
        pattern = schedule_pattern

    # Insert the form data into the table (add start and end time)
    item_id = data_tree.insert("", "end", text=current_time, values=(page_id, access_token, num_iterations, max_workers, tag_id_name, input_start_date, input_end_date, start_time, end_time,  input_start_schedule_date, scheduled_time, display_throw, status,"", pattern))

    # Check if the scheduled date has passed
    if batch != "auto":
        scheduled_datetime = combine_date_time(input_start_schedule_date, scheduled_time)
        if scheduled_datetime <= datetime.now():
            # Change the color of the scheduled text to blue
            data_tree.item(item_id, tags=("blue_text",))
        
        # Apply the blue text tag to the scheduled date and time
        data_tree.tag_configure("blue_text", foreground="blue")


# Function to download the processed data
def download_data(tagged_conversations):
    # Ask user for file path to save the data
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    
    # If file path is not empty, save the data to the file
    if file_path:
        with open(file_path, "w") as file:
            for conv_id in tagged_conversations:
                file.write(f"{conv_id}\n")
        
        messagebox.showinfo("Download Successful", "Data downloaded successfully.")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Create main window
root = tk.Tk()
root.title("IT: Autotag App")

# Create a radio button variable
auto_run_var = tk.IntVar()

# Get the current directory of the script
current_dir = os.path.dirname(__file__)

# Specify the path to the logo image file relative to the current directory
icon_path = resource_path("img/plogo3.ico")

# Change the icon of the root window
root.iconbitmap(icon_path)

# Load the image
# plogo5 = resource_path("plogo5.png")
image_path = resource_path("plogo5.png")
image = tk.PhotoImage(file=image_path)

# Create a label to display the image
image_label = ttk.Label(root, image=image)
image_label.grid(row=0, column=0, padx=(10, 5), pady=(20, 10), sticky=tk.W)

# Create a label for the text under the root title
center_label = ttk.Label(root, text="", font=("Helvetica", 14))
center_label.grid(row=0, column=1, columnspan=2, pady=(20, 10), sticky=tk.W)

# Create form
form = ttk.Frame(root, padding="20")
form.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E))


# Page ID
page_id_label = ttk.Label(form, text="Page ID:")
page_id_label.grid(row=0, column=0, sticky=tk.W)
page_id_entry = ttk.Entry(form)
page_id_entry.grid(row=0, column=1, sticky=tk.W)

# Access Token
access_token_label = ttk.Label(form, text="Access Token:")
access_token_label.grid(row=1, column=0, sticky=tk.W)
access_token_entry = ttk.Entry(form)
access_token_entry.grid(row=1, column=1, sticky=tk.W)

# Number of Iterations
num_iterations_label = ttk.Label(form, text="Number of Iterations:")
num_iterations_label.grid(row=2, column=0, sticky=tk.W)
num_iterations_entry = ttk.Entry(form)
num_iterations_entry.insert(0, "100")
num_iterations_entry.grid(row=2, column=1, sticky=tk.W)

# Maximum Workers
max_workers_label = ttk.Label(form, text="Maximum Workers:")
max_workers_label.grid(row=3, column=0, sticky=tk.W)
max_workers_entry = ttk.Entry(form)
max_workers_entry.insert(0, "1")
max_workers_entry.grid(row=3, column=1, sticky=tk.W)

#default Value of Tag
current_date = datetime.now()

# Get the month and day
month = current_date.strftime("%b").upper()  # Get the first 3 letters of the month in uppercase
day = current_date.strftime("%#d")  # Get the day

# Default Tag Name
default_tag_name = f"{month}{day}{'FF'}"
# default_tag_name = f"{month}{day}{'TEST'}"

# Tag ID Name
tag_id_to_add_label = ttk.Label(form, text="Tag Id Name:")
tag_id_to_add_label.grid(row=4, column=0, sticky=tk.W)
tag_id_to_add_entry = ttk.Entry(form)
tag_id_to_add_entry.insert(0, default_tag_name)
tag_id_to_add_entry.grid(row=4, column=1, sticky=tk.W)

#Shift Tag
#AM Shift Radio Button Tag
shift_label = ttk.Label(form, text="Shift:")
shift_label.grid(row=5, column=0, sticky=tk.W) 
shift_var = tk.IntVar()
am_shift_radiobutton = Radiobutton(form, text="AM Shift", variable=shift_var, value=1, command=toggle_shift)
am_shift_radiobutton.grid(row=5, column=1, sticky=tk.W, pady=10)

#PM Shift Radio Button Tag
pm_shift_radiobutton = Radiobutton(form, text="PM Shift", variable=shift_var, value=0, command=toggle_shift)
pm_shift_radiobutton.grid(row=5, column=2, sticky=tk.W, pady=10)

# Set default radio button selection
shift_var.set(1)

#Batch Throw
#1ST FF Throw 3 days Ago(AM) & Today @5 PM (PM)
first_ff_var = tk.IntVar()
first_ff_checkbox = Checkbutton(form, text ="1st Throw (3 days ago)", variable=first_ff_var , onvalue=1, offvalue=0, command=toggle_batch_throw)
first_ff_checkbox.grid(row=6, column=1, sticky=tk.W)

#2ND FF Throw 10 days Ago(AM) & Today @8 PM (PM)
second_ff_var = tk.IntVar()
second_ff_checkbox = Checkbutton(form, text ="2nd Throw (10 days ago)", variable=second_ff_var , onvalue=1, offvalue=0, command=toggle_batch_throw)
second_ff_checkbox.grid(row=6, column=2, sticky=tk.W)

#3RD FF Throw 30 days Ago(AM) & Today @12MN/AM (PM)
third_ff_var = tk.IntVar()
third_ff_checkbox = Checkbutton(form, text ="3rd Throw (30 days ago)", variable=third_ff_var , onvalue=1, offvalue=0, command=toggle_batch_throw)
third_ff_checkbox.grid(row=6, column=3, sticky=tk.W)

#Custom FF Throw
custom_ff_var = tk.IntVar()
custom_ff_checkbox = Checkbutton(form, text ="Custom", variable=custom_ff_var , onvalue=1, offvalue=0, command=toggle_batch_throw)
custom_ff_checkbox.grid(row=7, column=1, sticky=tk.W)

#Custome Date & Time Range Throw FF
# Input Start Date
input_start_date_label = ttk.Label(form, text="Start Date (YYYY-MM-DD):")
input_start_date_label.grid_forget()
input_start_date_entry = ttk.Entry(form)
input_start_date_entry.grid_forget()
input_start_date_entry.config(state="disabled")


# Input End Date
input_end_date_label = ttk.Label(form, text="End Date (YYYY-MM-DD):")
input_end_date_label.grid_forget()
input_end_date_entry = ttk.Entry(form)
input_end_date_entry.grid_forget()
input_end_date_entry.config(state="disabled")

#Conversation Start Time Frame
time_frame = ttk.Frame(form)
time_frame.grid_forget()

# Input Start Time
input_start_time_label = ttk.Label(form, text="Start Time:")  # Updated label text
input_start_time_label.grid_forget()

# Start Hour Dropdown (24-hour format)
hour_options = [f"{hour:02d}" for hour in range(0, 24)]  # Hours from 0 to 23 for 24-hour format
input_start_hour_var = tk.StringVar()  # New: Variable to store selected hour
input_start_hour_combobox = ttk.Combobox(time_frame, textvariable=input_start_hour_var, state="readonly", width=5)  # New: Combobox widget
input_start_hour_combobox['values'] = hour_options  # New: Values for the dropdown
input_start_hour_combobox.current(0)  # New: Default selection
input_start_hour_combobox.grid(row=0, column=0, sticky=tk.W)
input_start_hour_combobox.config(state="disabled")

# Colon Label (Start Hour and Minute separator)
ttk.Label(time_frame, text=":").grid(row=0, column=1, sticky=tk.W)  # New

# Start Minute Dropdown
minute_options = [f"{minute:02d}" for minute in range(0, 60)]  # Minutes from 0 to 59
input_start_minute_var = tk.StringVar()  # New: Variable to store selected minute
input_start_minute_combobox = ttk.Combobox(time_frame, textvariable=input_start_minute_var, state="readonly", width=5)  # New: Combobox widget
input_start_minute_combobox['values'] = minute_options  # New: Values for the dropdown
input_start_minute_combobox.current(0)  # New: Default selection
input_start_minute_combobox.grid(row=0, column=2, sticky=tk.W)  # New
input_start_minute_combobox.config(state="disabled")

# Start Colon Label (Minute and Second separator)
ttk.Label(time_frame, text=":").grid(row=0, column=3, sticky=tk.W)  # New

# Start Second Dropdown
second_options = [f"{second:02d}" for second in range(0, 60)]  # Seconds from 0 to 59
input_start_second_var = tk.StringVar()  # New: Variable to store selected second
input_start_second_combobox = ttk.Combobox(time_frame, textvariable=input_start_second_var, state="readonly", width=5)  # New: Combobox widget
input_start_second_combobox['values'] = second_options  # New: Values for the dropdown
input_start_second_combobox.current(0)  # New: Default selection
input_start_second_combobox.grid(row=0, column=4, sticky=tk.W)  # New
input_start_second_combobox.config(state="disabled")

#Conversation End Time Frame
end_time_frame = ttk.Frame(form)
end_time_frame.grid_forget()

# Input End Time 
input_end_time_label = ttk.Label(form, text="End Time:")  # Updated label text
input_end_time_label.grid_forget()  # New

# End Hour Dropdown (24-hour format)
hour_options = [f"{hour:02d}" for hour in range(0, 24)]  # Hours from 0 to 23 for 24-hour format
input_end_hour_var = tk.StringVar()  # New: Variable to store selected hour
input_end_hour_combobox = ttk.Combobox(end_time_frame, textvariable=input_end_hour_var, state="readonly", width=5)  # New: Combobox widget
input_end_hour_combobox['values'] = hour_options  # New: Values for the dropdown
input_end_hour_combobox.current(0)  # New: Default selection
input_end_hour_combobox.grid(row=0, column=0, sticky=tk.W)  # New
input_end_hour_combobox.config(state="disabled")

# Colon Label (End Hour and Minute separator)
ttk.Label(end_time_frame, text=":").grid(row=0, column=1, sticky=tk.W)  # New

# End Minute Dropdown
minute_options = [f"{minute:02d}" for minute in range(0, 60)]  # Minutes from 0 to 59
input_end_minute_var = tk.StringVar()  # New: Variable to store selected minute
input_end_minute_combobox = ttk.Combobox(end_time_frame, textvariable=input_end_minute_var, state="readonly", width=5)  # New: Combobox widget
input_end_minute_combobox['values'] = minute_options  # New: Values for the dropdown
input_end_minute_combobox.current(0)  # New: Default selection
input_end_minute_combobox.grid(row=0, column=2, sticky=tk.W)  # New
input_end_minute_combobox.config(state="disabled")

# End Colon Label (Minute and Second separator)
ttk.Label(end_time_frame, text=":").grid(row=0, column=3, sticky=tk.W)  # New

# End Second Dropdown End Conversational Time
second_options = [f"{second:02d}" for second in range(0, 60)]  # Seconds from 0 to 59
input_end_second_var = tk.StringVar()  # New: Variable to store selected second
input_end_second_combobox = ttk.Combobox(end_time_frame, textvariable=input_end_second_var, state="readonly", width=5)  # New: Combobox widget
input_end_second_combobox['values'] = second_options  # New: Values for the dropdown
input_end_second_combobox.current(0)  # New: Default selection
input_end_second_combobox.grid(row=0, column=4, sticky=tk.W)  # New
input_end_second_combobox.config(state="disabled")

# Auto Run Radio Button
auto_run_label = ttk.Label(form, text="Run Immediately?")
auto_run_label.grid(row=12, column=0, sticky=tk.W, pady=5)  # Updated row position
auto_run_radio1 = Radiobutton(form, text="Yes", variable=auto_run_var, value=1, command=toggle_auto_run)
auto_run_radio1.grid(row=12, column=1, sticky=tk.W, pady=5)  # Updated row position
auto_run_radio2 = Radiobutton(form, text="No", variable=auto_run_var, value=0, command=toggle_auto_run)
auto_run_radio2.grid(row=12, column=2, sticky=tk.W, pady=5)  # Updated row position

sched_date_frame = ttk.Frame(form)
sched_date_frame.grid(row=13, column=1, columnspan=6, sticky=tk.W, pady=4)

# Input Schedule Date  # New
input_schedule_date_label = ttk.Label(form, text="Schedule Date:")  # New
input_schedule_date_label.grid(row=13, column=0, sticky=tk.W)  # New
#Start Schedule Date
input_start_schedule_date_entry = DateEntry(sched_date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)  # New: DateEntry widget  # New
input_start_schedule_date_entry.grid(row=0, column=0, sticky=tk.W)  # New
ttk.Label(sched_date_frame, text=" to ").grid(row=0, column=1, sticky=tk.W)
#End Schedule Date
input_end_schedule_date_entry = DateEntry(sched_date_frame, width=12, background='darkblue', foreground='white', borderwidth=2)  # New: DateEntry widget  # New
input_end_schedule_date_entry.grid(row=0, column=2, sticky=tk.W)  # New

# Pattern Schedule Dropdown
ttk.Label(sched_date_frame, text=" ").grid(row=0, column=3, sticky=tk.W)
schedule_pattern_options = ["Once", "Weekly", "Everyday"]
input_schedule_pattern_var = tk.StringVar()  # New: Variable to store selected Schedule Pattern
input_schedule_pattern_combobox = ttk.Combobox(sched_date_frame, textvariable=input_schedule_pattern_var, state="readonly", width=10)  # New: Combobox widget
input_schedule_pattern_combobox['values'] = schedule_pattern_options  # New: Values for the dropdown
input_schedule_pattern_combobox.current(0)  # New: Default selection
input_schedule_pattern_combobox.grid(row=0, column=4, sticky=tk.W)  # New
input_schedule_pattern_combobox.bind("<<ComboboxSelected>>", toggle_schedule )

#Weekly Schdule Pattern
ttk.Label(sched_date_frame, text=" ").grid(row=0, column=5, sticky=tk.W)
weekly_label = ttk.Label(sched_date_frame, text="Every:")
weekly_label.grid_forget()
weekly_pattern_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
input_weekly_pattern_var = tk.StringVar()  # New: Variable to store selected Schedule Pattern
input_weekly_pattern_combobox = ttk.Combobox(sched_date_frame, textvariable=input_weekly_pattern_var, state="readonly", width=10)  # New: Combobox widget
input_weekly_pattern_combobox['values'] = weekly_pattern_options  # New: Values for the dropdown
input_weekly_pattern_combobox.current(0)  # New: Default selection
input_weekly_pattern_combobox.grid_forget()  # New

#DEFAULT WEEK
current_day_of_week = current_date.weekday()
input_weekly_pattern_combobox.current(current_day_of_week)

#Conversation Schedule Time Frame
sched_time_frame = ttk.Frame(form)
sched_time_frame.grid(row=14, column=1, columnspan=6, sticky=tk.W, pady=4)

# Input Schedule Time  # New
input_schedule_time_label = ttk.Label(form, text="Schedule Time:")  # New
input_schedule_time_label.grid(row=14, column=0, sticky=tk.W)  # New

# Hour Dropdown
hour_options = [f"{hour:02d}" for hour in range(1, 13)]  # Hours from 1 to 12
input_schedule_hour_var = tk.StringVar()  # New: Variable to store selected hour
input_schedule_hour_combobox = ttk.Combobox(sched_time_frame, textvariable=input_schedule_hour_var, state="readonly", width=5)  # New: Combobox widget
input_schedule_hour_combobox['values'] = hour_options  # New: Values for the dropdown
input_schedule_hour_combobox.current(0)  # New: Default selection
input_schedule_hour_combobox.grid(row=0, column=0, sticky=tk.W)  # New

# Colon Label
first_sched1 = ttk.Label(sched_time_frame, text=":")
first_sched1.grid(row=0, column=1, sticky=tk.W)  # New

# Minute Dropdown
minute_options = [f"{minute:02d}" for minute in range(0, 60, 1)]  # Minutes from 0 to 55 with 5-minute intervals
input_schedule_minute_var = tk.StringVar()  # New: Variable to store selected minute
input_schedule_minute_combobox = ttk.Combobox(sched_time_frame, textvariable=input_schedule_minute_var, state="readonly", width=5)  # New: Combobox widget
input_schedule_minute_combobox['values'] = minute_options  # New: Values for the dropdown
input_schedule_minute_combobox.current(0)  # New: Default selection
input_schedule_minute_combobox.grid(row=0, column=2, sticky=tk.W)  # New

# AM/PM Dropdown
ampm_options = ["AM", "PM"]
input_schedule_ampm_var = tk.StringVar()  # New: Variable to store selected AM/PM
input_schedule_ampm_combobox = ttk.Combobox(sched_time_frame, textvariable=input_schedule_ampm_var, state="readonly", width=3)  # New: Combobox widget
input_schedule_ampm_combobox['values'] = ampm_options  # New: Values for the dropdown
input_schedule_ampm_combobox.current(0)  # New: Default selection
input_schedule_ampm_combobox.grid(row=0, column=3, sticky=tk.W)  # New

first_sched = ttk.Label(sched_time_frame, text="1st Throw Schedule Time")
first_sched.grid_forget()

# 2ND Throw PM Schedule
# Hour Dropdown
hour_options2 = [f"{hour:02d}" for hour in range(1, 13)]  # Hours from 1 to 12
input_schedule_hour_var2 = tk.StringVar()  # New: Variable to store selected hour
input_schedule_hour_combobox2 = ttk.Combobox(sched_time_frame, textvariable=input_schedule_hour_var2, state="readonly", width=5)  # New: Combobox widget
input_schedule_hour_combobox2['values'] = hour_options2  # New: Values for the dropdown
input_schedule_hour_combobox2.current(0)  # New: Default selection
input_schedule_hour_combobox2.grid_forget()  # New

# Colon Label
second_sched1 = ttk.Label(sched_time_frame, text=":")
second_sched1.grid_forget() # New

# Minute Dropdown
minute_options2 = [f"{minute:02d}" for minute in range(0, 60, 1)]  # Minutes from 0 to 55 with 5-minute intervals
input_schedule_minute_var2 = tk.StringVar()  # New: Variable to store selected minute
input_schedule_minute_combobox2 = ttk.Combobox(sched_time_frame, textvariable=input_schedule_minute_var2, state="readonly", width=5)  # New: Combobox widget
input_schedule_minute_combobox2['values'] = minute_options2  # New: Values for the dropdown
input_schedule_minute_combobox2.current(0)  # New: Default selection
input_schedule_minute_combobox2.grid_forget() # New

# AM/PM Dropdown
ampm_options2 = ["AM", "PM"]
input_schedule_ampm_var2 = tk.StringVar()  # New: Variable to store selected AM/PM
input_schedule_ampm_combobox2 = ttk.Combobox(sched_time_frame, textvariable=input_schedule_ampm_var2, state="readonly", width=3)  # New: Combobox widget
input_schedule_ampm_combobox2['values'] = ampm_options2  # New: Values for the dropdown
input_schedule_ampm_combobox2.current(0)  # New: Default selection
input_schedule_ampm_combobox2.grid_forget()  # New

second_sched = ttk.Label(sched_time_frame, text="2nd Throw Schedule Time")
second_sched.grid_forget()

# 3RD Throw PM Schedule
# Hour Dropdown
hour_options3 = [f"{hour:02d}" for hour in range(1, 13)]  # Hours from 1 to 12
input_schedule_hour_var3 = tk.StringVar()  # New: Variable to store selected hour
input_schedule_hour_combobox3 = ttk.Combobox(sched_time_frame, textvariable=input_schedule_hour_var3, state="readonly", width=5)  # New: Combobox widget
input_schedule_hour_combobox3['values'] = hour_options3  # New: Values for the dropdown
input_schedule_hour_combobox3.current(0)  # New: Default selection
input_schedule_hour_combobox3.grid_forget()# New

# Colon Label
third_sched1 = ttk.Label(sched_time_frame, text=":")
third_sched1.grid_forget()  # New

# Minute Dropdown
minute_options3 = [f"{minute:02d}" for minute in range(0, 60, 1)]  # Minutes from 0 to 55 with 5-minute intervals
input_schedule_minute_var3 = tk.StringVar()  # New: Variable to store selected minute
input_schedule_minute_combobox3 = ttk.Combobox(sched_time_frame, textvariable=input_schedule_minute_var3, state="readonly", width=5)  # New: Combobox widget
input_schedule_minute_combobox3['values'] = minute_options3  # New: Values for the dropdown
input_schedule_minute_combobox3.current(0)  # New: Default selection
input_schedule_minute_combobox3.grid_forget() # New

# AM/PM Dropdown
ampm_options3 = ["AM", "PM"]
input_schedule_ampm_var3 = tk.StringVar()  # New: Variable to store selected AM/PM
input_schedule_ampm_combobox3 = ttk.Combobox(sched_time_frame, textvariable=input_schedule_ampm_var3, state="readonly", width=3)  # New: Combobox widget
input_schedule_ampm_combobox3['values'] = ampm_options3  # New: Values for the dropdown
input_schedule_ampm_combobox3.current(0)  # New: Default selection
input_schedule_ampm_combobox3.grid_forget()  # New

third_sched = ttk.Label(sched_time_frame, text="3rd Throw Schedule Time")
third_sched.grid_forget()

toggle_schedule_entry_widgets(input_start_schedule_date_entry, input_end_schedule_date_entry, input_schedule_hour_combobox, input_schedule_minute_combobox, input_schedule_ampm_combobox, input_schedule_hour_combobox2, input_schedule_minute_combobox2, input_schedule_ampm_combobox2, input_schedule_hour_combobox3, input_schedule_minute_combobox3, input_schedule_ampm_combobox3)


# Set default radio button selection
auto_run_var.set(0)

# Submit Button
submit_button = ttk.Button(form, text="Submit", command=submit_form)
submit_button.grid(row=15, column=0, pady=10)  # Adjusted row position

# Download Button
download_button = ttk.Button(form, text="Download Data", command=lambda: download_data(None), state="disabled")
download_button.grid(row=15, column=1, pady=10)  # Adjusted row position

# Progress bar
progress_bar = ttk.Progressbar(form, orient="horizontal", length=200, mode="determinate")
progress_bar.grid(row=16, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))

progress_bar_label = tk.Label(form, text="0%")
progress_bar_label.grid(row=16, column=2, sticky=tk.W)

# Create container for running data
running_data_frame = ttk.Frame(root, padding="20")
running_data_frame.grid(row=1, column=2, sticky=(tk.N, tk.W, tk.E, tk.S))  # Adjust column to 2

# Running Data Text
running_data_text = tk.Text(running_data_frame, wrap="word", height=5, width=40)
running_data_text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

# Configure grid weights for resizing
running_data_frame.grid_rowconfigure(0, weight=1)
running_data_frame.grid_columnconfigure(0, weight=1)

# Create a treeview for displaying the data in a table format
# add conversational time
data_tree = ttk.Treeview(root, columns=("Page ID", "Access Token", "Iterations", "Max Workers", "Tag Name", "Start Date", "End Date","Start Time", "End Time", "Scheduled Date", "Scheduled Time", "Batch", "Status", "Total Successful Toggles", "Schedule"))  # # Updated: Added columns for Scheduled Time, Status, and Total Successful Toggles, Added columns for Scheduled Time and Status
data_tree.heading("#0", text="ID")
data_tree.heading("Page ID", text="Page ID")
data_tree.heading("Access Token", text="Access Token")
data_tree.heading("Iterations", text="Iterations")
data_tree.heading("Max Workers", text="Max Workers")
data_tree.heading("Tag Name", text="Tag Name")
data_tree.heading("Start Date", text="Start Date")
data_tree.heading("End Date", text="End Date")
data_tree.heading("Start Time", text="Start Time")
data_tree.heading("End Time", text="End Time")
data_tree.heading("Scheduled Date", text="Scheduled Date")
data_tree.heading("Scheduled Time", text="Scheduled Time")
data_tree.heading("Batch", text="Batch")
data_tree.heading("Status", text="Status")
data_tree.heading("Total Successful Toggles", text="Total Tags")
data_tree.heading("Schedule", text="Schedule")  # New column
data_tree.column("#0", stretch=tk.NO, minwidth=0, width=0)
data_tree.column("Page ID", stretch=tk.NO, minwidth=100, width=100)
data_tree.column("Access Token", stretch=tk.NO, minwidth=140, width=140)
data_tree.column("Iterations", stretch=tk.NO, minwidth=80, width=80)
data_tree.column("Max Workers", stretch=tk.NO, minwidth=80, width=90)
data_tree.column("Tag Name", stretch=tk.NO, minwidth=80, width=90)
data_tree.column("Start Date", stretch=tk.NO, minwidth=90, width=90)
data_tree.column("End Date", stretch=tk.NO, minwidth=90, width=90)
data_tree.column("Start Time", stretch=tk.NO, minwidth=80, width=90)
data_tree.column("End Time", stretch=tk.NO, minwidth=80, width=90)
data_tree.column("Scheduled Date", stretch=tk.NO, minwidth=90, width=100)
data_tree.column("Scheduled Time", stretch=tk.NO, minwidth=90, width=100)
data_tree.column("Batch", stretch=tk.NO, minwidth=75, width=80)
data_tree.column("Status", stretch=tk.NO, minwidth=80, width=90)
data_tree.column("Total Successful Toggles", stretch=tk.NO, minwidth=120, width=120) 
data_tree.column("Schedule", stretch=tk.NO, minwidth=80, width=100) # New column

# Apply tag with blue font color to values in the "Status" column
data_tree.tag_configure("blue_status", foreground="blue")

# Apply the tag to the values in the "Status" column
data_tree.tag_bind("blue_status", sequence="<<TreeviewSelect>>", callback=lambda event: None)

data_tree.grid(row=3, column=0, columnspan=4, pady=10)

# Add a button to update the table with the form data
update_table_button = ttk.Button(form, text="Edit Schedule", command = edit_table)
update_table_button.grid(row=17, column=0, columnspan=1, pady=10)
stop_table_button = ttk.Button(form, text="Stop Schedule", command=stop_scheduled_tag)
stop_table_button.grid(row=17, column=1, columnspan=1, pady=10)

# Start GUI event loop
root.mainloop()
