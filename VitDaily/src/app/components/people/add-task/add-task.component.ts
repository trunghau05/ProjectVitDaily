import { Component, EventEmitter, OnInit, Input, Output, signal } from '@angular/core';
import { Task } from '../../../models/people/task.interface';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { TaskService } from '../../../services/people/task.service';
import { WorkSpace } from '../../../models/people/workspace.interface';
import { Team } from '../../../models/people/team.interface';

@Component({
  selector: 'app-add-task',
  imports: [CommonModule, MatIconModule, FormsModule],
  templateUrl: './add-task.component.html',
  styleUrl: './add-task.component.scss'
})
export class AddTaskComponent implements OnInit {
  @Input() workspace = signal<WorkSpace | null>(null);
  @Input() tsId: string | null = null;
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
    owner_id: '',
    tm_id: '',
    assignees: [],
    subtasks: []
  }

  ownerId: string | undefined;

  constructor(private taskService: TaskService) {}

  ngOnInit(): void {
    this.ownerId = this.workspace()?.owner_id;    
    if (this.ownerId && this.tsId) {
      this.task.owner_id = this.ownerId;
      this.task.tm_id = this.tsId;
    }
  }

  private validateTask(task: Task): string | null {
    if (!task.ts_title || task.ts_title.trim() === '') return 'Tiêu đề task không được để trống.';
    if (!task.ts_start || !task.ts_end) return 'Ngày bắt đầu và kết thúc phải được chọn.';
    if (!task.owner_id || task.owner_id.trim() === '') return 'Owner task không xác định.';
    return null; 
  }

  async addTask() {
    const error = this.validateTask(this.task);
    if (error) {
      alert(error);
      return;
    }

    try {
      const response = await this.taskService.addTasks([this.task]); 
      
      if (response && Array.isArray(response.tasks) && response.tasks.length > 0) {
        alert('Thêm công việc thành công: ' + response.tasks[0].ts_id);
      } else {
        alert('Thêm công việc thành công!');
      }

      this.closeAdd();
    } catch (error) {
      console.error(error);
      alert('Lỗi khi thêm task!');
    }
  }

  closeAdd() {
    this.close.emit();
  }
}