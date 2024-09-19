



#!/usr/bin/python3
import subprocess, sys

class BackupScript(): #automatically backup folder (origin_directory) in chosen directory (backups_directory)
    def __init__(self):
        self.config_reading() #retrieving origin_directory and backup_directory from BackupScript.config

        if self.origin_directory == '' or self.backup_directory == '':
            self.command = str(input("[-] Wrong paths\nDo you you want to set up new paths? [y/n] "))
            if self.command == 'y':
                self.directories_set_up() #adding new origin_directory and backup_directory
                
            else:
                self.config.close() #shutting BackupScript.config
                sys.exit #interrupt execution of this programm
                
            self.config.close() #shutting BackupScript.config
            self.execution() #creating name for backup, performing backup
            self.cheking_result()
            
        else:
            self.command = str(input("Do you want to change paths? [y/n] "))
            if self.command == 'y':
                self.new_paths_set_up() #adding new origin_directory and backup_directory
                self.config.close() #shutting BackupScript.config
                self.execution() #creating name for backup, performing backup
                self.cheking_result()
                
            elif self.command == 'n':
                self.config.close() #shutting BackupScript.config
                self.execution() #creating name for backup, performing backup
                self.cheking_result()
                
            else:
                self.config.close() #shutting BackupScript.config
                sys.exit #interrupt execution of this programm


    def config_reading(self): #retrieving origin_directory and backup_directory from BackupScript.config
        try:
            self.config = open("BackupScript.config", "r")
        except:
            self.config = open("BackupScript.config", "a+")
                    
        self.origin_directory = self.config.readline().replace("\n", "") # directory with files for backups
        self.backup_directory = self.config.readline().replace("\n", "") # directory for backups

    
    def directories_set_up(self): #adding new origin_directory and backup_directory
        self.origin_directory = str(input("Please, enter path to directory with files for backups "))
        self.backup_directory = str(input("Please, enter path to directory of backups "))
        self.config.truncate() #complete file purge
        self.config.write(self.origin_directory + "\n" + self.backup_directory) #adding new origin_directory and backup_directory in BackupScript.config

        
    def execution(self): #creating name for backup, performing backup
        self.current_date = subprocess.check_output("date +%Y:%m:%d-%H:%M:%S", shell=True).decode().replace("\n", "") #receiving curent date and time from system
        self.backup_directory_name = "backup-" + self.current_date #creating name for new backup with "backup-YYYY:MM:DD-hh-mm-ss" pattern

        if self.origin_directory.split('/')[-1] == '': #retrieving last folder title from origin_directory
            self.origin_directory_name = self.origin_directory.split('/')[-2]
        else:
            self.origin_directory_name = self.origin_directory.split('/')[-1]
        
        subprocess.run(["cp", "-r", self.origin_directory, self.backup_directory]) #copying files from source to new backup folder
        subprocess.run(["mv", self.backup_directory + self.origin_directory_name, self.backup_directory + self.backup_directory_name]) #renaming new backup folder from old name to backup_directory_name


    def cheking_result(self):
        backup_files = subprocess.check_output("ls " + self.backup_directory + self.backup_directory_name, shell=True).decode().split() #creating array with files and folders from new backup file
        source_files = subprocess.check_output("ls " + self.origin_directory, shell=True).decode().split() #creating array with files and folders from origin_directory

        for title in source_files: #comparing backup_files and source_files
            if title in backup_files:
                pass
            else:
                print("[-] Something went wrong")
                sys.exit #interrupt execution of this programm
        print("[+] The backup was successful")
        sys.exit #interrupt execution of this programm
        
            
backup = BackupScript()

