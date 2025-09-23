import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { MatIconModule } from '@angular/material/icon';
import { CommonModule } from '@angular/common';
import { CdkDragDrop, moveItemInArray, transferArrayItem, CdkDrag, CdkDropList, } from '@angular/cdk/drag-drop';
import { SearchBarComponent } from '../../../components/search-bar/search-bar.component';

@Component({
  selector: 'app-task',
  imports: [NavbarComponent, FlexCenterDirective, MatIconModule, CommonModule, CdkDrag, CdkDropList, SearchBarComponent],
  templateUrl: './task.component.html',
  styleUrl: './task.component.scss'
})
export class TaskComponent implements OnInit{
  isKanban: boolean = false;
  isList: boolean = true;

  tasks: any[] = [];
  todo: any[] = [];
  doing: any[] = [];
  done: any[] = [];

  ngOnInit() {
    this.tasks = [
      {
        title: 'Đây là tiêu đề công việc',
        content: 'Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc.',
        status: 1
      },
      {
        title: 'Đây là tiêu đề công việc',
        content: 'Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc.',
        status: 2
      },
      {
        title: 'Đây là tiêu đề công việc',
        content: 'Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc.',
        status: 0
      },
      {
        title: 'Đây là tiêu đề công việc',
        content: 'Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc.',
        status: 1
      },
      {
        title: 'Đây là tiêu đề công việc',
        content: 'Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc.',
        status: 1
      },
      {
        title: 'Đây là tiêu đề công việc',
        content: 'Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc. Đây là nội dung công việc.',
        status: 2
      },
    ];

    this.todo = this.tasks.filter(task => task.status === 0);
    this.doing = this.tasks.filter(task => task.status === 1);
    this.done = this.tasks.filter(task => task.status === 2);
  }

  toggleList() {
    this.isList = true;
    this.isKanban = false;
  }

  toggleKanban() {
    this.isKanban = true;
    this.isList = false;
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
      if (this.todo.includes(task)) task.status = 0;
      if (this.doing.includes(task)) task.status = 1;
      if (this.done.includes(task)) task.status = 2;
    });
  }

}
