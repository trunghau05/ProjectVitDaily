import { CommonModule } from '@angular/common';
import { Component, Input, OnInit, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { Member, WorkSpace } from '../../../models/people/workspace.interface';
import { ActivatedRoute } from '@angular/router';
import { WorkspaceService } from '../../../services/people/workspace.service';
import { TeamService } from '../../../services/people/team.service';
import { Team } from '../../../models/people/team.interface';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { MatIconModule } from '@angular/material/icon';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { Task } from '../../../models/people/task.interface';
import { TaskService } from '../../../services/people/task.service';
import { SearchBarComponent } from '../../../components/search-bar/search-bar.component';
import { AddTaskComponent } from '../../../components/people/add-task/add-task.component';
import { DetailTaskComponent } from '../../../components/people/detail-task/detail-task.component';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-team',
  imports: [CommonModule, FormsModule, NavbarComponent, FlexCenterDirective, MatIconModule, FormatDatePipe, FlexCenterDirective, SearchBarComponent, AddTaskComponent, DetailTaskComponent],
  templateUrl: './team.component.html',
  styleUrl: './team.component.scss'
})
export class TeamComponent implements OnInit{
  wsId: string | null = null;
  today = new Date;
  tsId = '';
  email = '';
  role = '';
  teamName = '';

  workspace = signal<WorkSpace | null>(null);
  teams = signal<Team[]>([]);
  teamSelect = {} as Team;
  newTeam = {} as Team;
  tasks = signal<Task[]>([]);
  members = signal<Member[]>([]);
  newMembers = signal<Member[]>([]);
  displayedTasks = signal<Task[]>([]);
  selectedTeam = signal<string | null>(null);

  pageSize = 10;
  currentPage = 0;
  loading = false;
  isKanban: boolean = false;
  isList: boolean = true;
  isDetail: boolean = false;
  isAdd: boolean = false;
  isUpdate: boolean = false;
  isDisconnect: boolean = false;
  isTeam: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private workspaceService: WorkspaceService,
    private teamService: TeamService,
    private taskService: TaskService,
    private userService: UserService,
  ) {}

  ngOnInit(): void {
    this.wsId = this.route.snapshot.paramMap.get('ws_id');
    this.loadPage();
  }

  async selectTeam(team: Team) {
    if (this.selectedTeam() === team.tm_id) {
      this.selectedTeam.set(null);
    } else {
      this.selectedTeam.set(team.tm_id);
      try {
        const response = await this.teamService.getTeamDetail(team.tm_id);
        this.teamSelect = response.data;
        this.members.set(this.teamSelect.members);
        this.close();
        this.tsId = this.teamSelect.tm_id;

      } catch (error) {
        console.error("Lỗi khi lấy thông tin nhóm", error);
      }
      this.getTaskList(team.tm_id);
    }
  }

  toggleList() {
    this.isList = true;
    this.isKanban = false;
  }

  toggleKanban() {
    this.isKanban = true;
    this.isList = false;
  }

  toggleTeam() {
    this.isTeam = !this.isTeam;
    this.newMembers.set([]);
    this.teamName = '';
  }

  close() {
    this.isTeam = false;
    this.newMembers.set([]);
    this.teamName = '';
  }

  removeMember(index: number) {
    const currentUser = sessionStorage.getItem('us_id');
    if(currentUser != this.workspace()?.owner_id) {
      return;
    } else {
      this.members().splice(index, 1);
      this.isUpdate = true;
    }
  }

  async disconnectTeam() {
    const currentUser = sessionStorage.getItem('us_id');
    if (currentUser == this.workspace()?.owner_id) {

      const ok = window.confirm("Bạn có chắc muốn xóa team này không?");
      if (!ok) return; 

      try {
        const response = await this.teamService.deleteTeam(this.teamSelect.tm_id);
        alert("Xóa team thành công!");
      } catch (error) {
        console.error(error);
      }
    } else {
      const updateMembers = this.members().filter(m => m.us_id != currentUser);
      this.teamSelect.members = updateMembers;
      this.updateTeam();
    }
    this.ngOnInit();
  }

  async addUserByEmail() {
    try {
      const response = await this.userService.getUserByEmail(this.email);
      const user = response;      
      const today = new Date();

      if (user) {
        const member: Member = {
          us_id: user.us_id,
          us_name: user.us_name,
          us_img: user.us_img,
          role: this.role || 'member',
          joined_at: today.toISOString()
        };

        const existed = this.workspace()?.members?.find(m => m.us_id === member.us_id);
        if (!existed) {
          alert("Người dùng này không có trong Workspace!");
          this.email = '';
          this.role = '';
          return;
        }

        this.members().push(member);
        this.newMembers().push(member);
        this.updateTeam();

        this.email = '';
        this.role = '';
      }
    } catch (error) {
      console.error("Lỗi khi lấy user theo email:", error);
    }
  }

  async addTeam() {
    if(!this.wsId) return;

    this.newTeam.ws_id = this.wsId;
    this.newTeam.members = this.newMembers();
    this.newTeam.tm_name = this.teamName;
    this.newTeam.created_at = this.today.toISOString();

    try {
      const response = await this.teamService.addTeam(this.newTeam);
      console.log(response);
      this.closeAdd;
      this.ngOnInit();
    } catch (error) {
      console.error("Lỗi khi thêm nhóm", error);
    }
  }

  async loadPage() {
    if (!this.wsId) return;

    try {
      const response = await this.workspaceService.getWorkspaceDetail(this.wsId);
      this.workspace.set(response.data);
    } catch (error) {
      console.error("Lỗi khi lấy chi tiết Workspace:", error);
    }

    try {
      const response = await this.teamService.getTeamByWorkspace(this.wsId);
      this.teams.set(response.data);

      if(this.teams().length > 0) {
        const first = this.teams()[0];
        this.selectTeam(first);
      }
    } catch (error) {
      console.error("Lỗi khi lấy danh sách Team:", error);
    }
  }

  async getTaskList(tm_id: string | '') {
    if (!tm_id) return;

    this.tasks.set([]);
    this.displayedTasks.set([]);
    this.currentPage = 0;

    try {
      const response = await this.taskService.getTaskList(tm_id);
      this.tasks.set(response.tasks);  
      this.displayedTasks.set([]);    
      this.currentPage = 0;
      this.loadMoreTasks();
    } catch (error) {
      console.error(`Lỗi khi lấy danh sách tasks của team ${tm_id}`, error);
    }
  }

  async updateTeam() {
    if(!this.teamSelect.tm_id) return;
    console.log("team select: ", this.teamSelect);
    
    try {
      const response = await this.teamService.updateTeam(this.teamSelect.tm_id, this.teamSelect);      
      this.isUpdate = false;
    } catch (error) {
      console.error("Lỗi khi cập nhật team", error);
    }
  }

  loadMoreTasks() {
    const start = this.currentPage * this.pageSize;
    const end = start + this.pageSize;
    const tasksSlice = this.tasks().slice(start, end);
    if (tasksSlice.length === 0) return; 

    this.displayedTasks.update(current => [...current, ...tasksSlice]);

    console.log('Displayed tasks:', this.displayedTasks());
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
      }, 300);
    }
  }

  onStatusChange(task: Task, newStatus: number) {
    task.ts_status = newStatus;   
    this.updateTask(task);   
    this.getTaskList(this.teamSelect.tm_id);    
  }

  async updateTask(task: Task) {
    try {
      const response = await this.taskService.updateTask(task.ts_id, task);
    } catch (error) {
      console.error("Lỗi khi cập nhật status", error);
    }
  }

  getStatusText(status: number) {
    switch (status) {
      case 0: return 'Chưa bắt đầu';
      case 1: return 'Đang tiến hành';
      case 2: return 'Đã hoàn thành';
      default: return 'Không xác định';
    }
  }

  getBackgroundColor(status: number) {
    switch (status) {
      case 0: return 'rgba(16, 73, 179, 0.2)';
      case 1: return 'rgba(180, 162, 0, 0.2)';
      case 2: return 'rgba(0, 128, 0, 0.2)';
      default: return 'white';
    }
  }

  detailTask(ts_id: string) {
    this.tsId = ts_id;
    this.isDetail = true;
  }

  addTask() {
    this.isAdd = true;
  }

  closeAdd() {
    this.isAdd = false;
  }

  closeDetail() {
    this.isDetail = false;
  }

  async onTaskSaved(updatedTask: Task): Promise<void> {
    await this.getTaskList(this.teamSelect.tm_id);
  }

  async onTaskDeleted(deletedId: string): Promise<void> {
    await this.getTaskList(this.teamSelect.tm_id);
  }
}
