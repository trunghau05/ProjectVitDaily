import { CommonModule, Location } from '@angular/common';
import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { TaskService } from '../../../services/people/task.service';
import { Task } from '../../../models/people/task.interface';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { Team } from '../../../models/people/team.interface';

@Component({
  selector: 'app-detail-task',
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './detail-task.component.html',
  styleUrl: './detail-task.component.scss'
})
export class DetailTaskComponent implements OnInit {
  @Input() tsId: string | null = null;
  @Input() team = {} as Team
  @Output() close = new EventEmitter<void>();
  @Output() saved = new EventEmitter<Task>();
  @Output() deleted = new EventEmitter<string>();

  task = {} as Task;
  isMem = false;

  ngOnInit() {
    this.detailTask();
  }

  constructor(private taskService: TaskService, private location: Location) {}

  async detailTask() {
    if(!this.tsId) return;
    try {
      const respone = await this.taskService.getTaskDetail(this.tsId);
      this.task = respone.task;
      this.task.assignees = this.task.assignees || [];      
    } catch (error) {
      console.error(error);
    }
  }

  toggleMem() {
    this.isMem = !this.isMem;
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

  addAssignee(m: any) {
    if (this.task.assignees.some(a => a.us_id === m.us_id)) return;
    this.task.assignees.push(m);
  }

  removeAssignee(m: any) {
    this.task.assignees = this.task.assignees.filter(a => a.us_id !== m.us_id);
  }

  closeDetail() {
    this.close.emit();
  }

  async saveTask() {
    try {
      await this.taskService.updateTask(this.task.ts_id, this.task);
      console.log('Task updated successfully');
      this.saved.emit(this.task);
      this.closeDetail();
    } catch (error) {
      console.error('Error saving task:', error);
    }
  }

  async deleteTask() {
    if (!confirm('Bạn có chắc chắn muốn xóa công việc này không?')) {
      return;
    }
    try {
      await this.taskService.deleteTask(this.task.ts_id);
      console.log('Task deleted successfully');
      this.deleted.emit(this.task.ts_id as string);
      this.closeDetail();
    } catch (error) {
      console.error('Error deleting task:', error);
    }
  }

  focusTask() {
    
  }
}
