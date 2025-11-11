import { CommonModule, Location } from '@angular/common';
import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { TaskService } from '../../../services/person/task.service';
import { Task } from '../../../models/task.interface';

@Component({
  selector: 'app-detail-task',
  imports: [CommonModule],
  templateUrl: './detail-task.component.html',
  styleUrl: './detail-task.component.scss'
})
export class DetailTaskComponent implements OnInit {
  @Input() tsId: string | null = null;

  task = {} as Task;

  ngOnInit() {
    this.detailTask();
  }

  constructor(private taskService: TaskService, private location: Location) {}

  async detailTask() {
    if(!this.tsId) return;
    try {
      const respone = await this.taskService.taskDetail(this.tsId);
      this.task = respone;
      console.log(this.task);
      
    } catch (error) {
      console.error(error);
    }
  }

  getStatusText(): string {
    switch(this.task.ts_status) {
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
