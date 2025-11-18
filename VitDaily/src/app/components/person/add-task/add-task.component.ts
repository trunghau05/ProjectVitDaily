import { Component, EventEmitter, OnInit, Input, Output } from '@angular/core';
import { Task } from '../../../models/person/task.interface';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { TaskService } from '../../../services/person/task.service';

@Component({
  selector: 'app-add-task',
  imports: [CommonModule, MatIconModule, FormsModule],
  templateUrl: './add-task.component.html',
  styleUrl: './add-task.component.scss'
})
export class AddTaskComponent implements OnInit {
  @Output() close = new EventEmitter<void>();
  @Output() add = new EventEmitter<Task>();

  task: Task = {
    ts_id: '',
    ts_title: '',
    ts_subtitle: '',
    ts_status: 0,
    ts_start: '',
    ts_end: '',
    ts_note: '',
    us_id: '',
  }

  usId: string | null = null;

  ngOnInit(): void {
      this.usId = sessionStorage.getItem('us_id');
      if(this.usId) {
        this.task.us_id = this.usId;
      }
      console.log(this.task.us_id);
      
  }

  constructor(private taskService: TaskService) {}

  async addTask() {
    try {
      const respone = await this.taskService.addTask(this.task);
      this.task = respone;
      alert('Thêm công việc thành công');
      this.closeAdd();
    } catch (error) {
      console.error(error);
    }
  }

  closeAdd() {
    this.close.emit();
  }
}
