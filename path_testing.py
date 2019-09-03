# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 14:22:05 2019

@author: Administrator
"""

from pathlib import Path



class files_():
    def __init__(self,data_dir):
        self.code_dir = Path().resolve()
        self.data_dir = Path(data_dir)
        if not self.data_dir.is_absolute():
            self.data_dir = self.code_dir/data_dir
        if not self.data_dir.exists():
            raise ValueError('Invalidate input path')
        self.old_file = ''
        self.new_file = ''
        # default setting on data folder, change it if u need
        self.files = list(self.data_dir.glob('*.mp4'))
        # select unprocessed files with the length of file name < 67 
        self.files = set([i for i in self.files if len(i.name) < 67])
        if self.files:
            self.file = self.files.pop()
        else:
            raise ValueError(f"没有可以处理的文件")
        

    def return_relative_dir(self):
        return self.file.relative_to(self.code_dir)
        
    def pop_update(self):
        if self.files:
            self.file = self.files.pop()
            return self.file
        else:
            raise ValueError(f"已经没有可以处理的文件")


if __name__ == '__main__':
    f = files_('C:/Users/Administrator/Documents/GitHub/ploty_dash/data')
    
