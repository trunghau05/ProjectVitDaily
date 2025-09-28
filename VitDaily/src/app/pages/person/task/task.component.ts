import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, moveItemInArray, transferArrayItem, CdkDrag, CdkDropList, } from '@angular/cdk/drag-drop';
import { SearchBarComponent } from '../../../components/search-bar/search-bar.component';
import { Task } from '../../../models/task.interface';
import { TaskService } from '../../../services/person/task.service';

@Component({
  selector: 'app-task',
  imports: [NavbarComponent, FlexCenterDirective, MatIconModule, CommonModule, CdkDrag, CdkDropList, SearchBarComponent],
  templateUrl: './task.component.html',
  styleUrl: './task.component.scss'
})
export class TaskComponent implements OnInit{
  isKanban: boolean = false;
  isList: boolean = true;
  usId = '';

  tasks: Task[] = [];
  todo: any[] = [];
  doing: any[] = [];
  done: any[] = [];

  async ngOnInit() {
    this.usId = sessionStorage.getItem('us_id') || '';
    await this.taskList();

    this.todo = this.tasks.filter(task => task.ts_status === 0); 
    this.doing = this.tasks.filter(task => task.ts_status === 1);
    this.done = this.tasks.filter(task => task.ts_status === 2);
  }

  constructor(private taskService: TaskService) {}

  toggleList() {
    this.isList = true;
    this.isKanban = false;
  }

  toggleKanban() {
    this.isKanban = true;
    this.isList = false;
  }

  async taskList() {
    try {
      const respone = await this.taskService.getTaskList(this.usId);
      this.tasks = respone;
      console.log(this.tasks);
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
      if (this.todo.includes(task)) task.ts_status = 0;
      if (this.doing.includes(task)) task.ts_status = 1;
      if (this.done.includes(task)) task.ts_status = 2;
    });
  }

  getStatus(status: number): string {
    switch (status) {
      case 0:
        return 'Chưa bắt đầu';
      case 1:
        return 'Đang tiến hành';
      case 2:
        return 'Đã hoàn thành';
      default:
        return 'Không xác định';
    }
  }
}
