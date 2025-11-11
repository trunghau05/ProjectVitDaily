import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, moveItemInArray, transferArrayItem, CdkDrag, CdkDropList, } from '@angular/cdk/drag-drop';
import { SearchBarComponent } from '../../../components/search-bar/search-bar.component';
import { Task } from '../../../models/task.interface';
import { TaskService } from '../../../services/person/task.service';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { DetailTaskComponent } from '../../../components/person/detail-task/detail-task.component';

@Component({
  selector: 'app-task',
  imports: [NavbarComponent, FlexCenterDirective, MatIconModule, CommonModule, CdkDrag, CdkDropList, SearchBarComponent, FormsModule, DetailTaskComponent],
  templateUrl: './task.component.html',
  styleUrl: './task.component.scss'
})
export class TaskComponent implements OnInit{
  isKanban: boolean = false;
  isList: boolean = true;
  isDetail: boolean = false;
  optionOpen: boolean = false;
  usId = '';
  tsId = '';

  tasks: Task[] = [];
  displayedTasks: Task[] = []; 
  pageSize: number = 10;    
  currentPage: number = 0;
  todo: any[] = [];
  doing: any[] = [];
  done: any[] = [];
  loading = false;

  async ngOnInit() {
    this.usId = sessionStorage.getItem('us_id') || '';
    await this.taskList();

    this.todo = this.tasks.filter(task => task.ts_status === 0); 
    this.doing = this.tasks.filter(task => task.ts_status === 1);
    this.done = this.tasks.filter(task => task.ts_status === 2);
  }

  constructor(private taskService: TaskService, private router: Router) {}

  toggleList() {
    this.isList = true;
    this.isKanban = false;
  }

  toggleKanban() {
    this.isKanban = true;
    this.isList = false;
  }

  loadMoreTasks() {
    const start = this.currentPage * this.pageSize;
    const end = start + this.pageSize;
    if (start >= this.tasks.length) return; 
    this.displayedTasks.push(...this.tasks.slice(start, end));
    this.currentPage++;
  }

  onScroll(event: any) {
    const div = event.target;
    const threshold = 50; 
    const atBottom = div.scrollHeight - (div.scrollTop + div.clientHeight) < threshold;
    
    if (atBottom && !this.loading) {
      this.loading = true;
      setTimeout(() => { 
        this.loadMoreTasks();
        this.loading = false;
      }, 500);
    }
  }

  async taskList() {
    try {
      const respone = await this.taskService.getTaskList(this.usId);
      this.tasks = respone;
      this.currentPage = 0;        
      this.displayedTasks = [];    
      this.loadMoreTasks();  
      console.log(this.tasks)            
    } catch (error) {
      Response.error;
    }
  }
 
  drop(event: CdkDragDrop<any[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(
        event.previousContainer.data,
        event.container.data,
        event.previousIndex,
        event.currentIndex
      );
    }

    event.container.data.forEach(task => {
      if (this.todo.includes(task)) {
        task.ts_status = 0;
        this.updateTask(task);
      }
      if (this.doing.includes(task)) {
        task.ts_status = 1;
        this.updateTask(task);
      }
      if (this.done.includes(task)) {
        task.ts_status = 2;
        this.updateTask(task);
      }
    });
  }

  async updateTask(task: any) {
    try {
      const respone = await this.taskService.updateTask(task.ts_id, task);
      console.log('Trạng thái của task ' + task.ts_id + ': ' + task.ts_status);
    } catch (error) {
      Response.error;
    }
  }

  getBackgroundColor(status: number) {
    switch(status) {
      case 0: return 'rgba(16, 73, 179, 0.2)';
      case 1: return 'rgba(180, 162, 0, 0.2)'; 
      case 2: return 'rgba(0, 128, 0, 0.2)';   
      default: return 'white';
    }
  }

  getStatusText(status: number) {
    switch(status) {
      case 0: return 'Chưa bắt đầu';
      case 1: return 'Đang tiến hành'; 
      case 2: return 'Đã hoàn thành';   
      default: return 'Không xác định';
    }
  }

  onStatusChange(task: Task, newStatus: number) {
    task.ts_status = newStatus;   
    this.updateTask(task);       
  }

  detailTask(ts_id: string) {
    this.tsId = ts_id;
    this.isDetail = true;
  }

  closeDetail() {
    this.isDetail = false;
  }
}
