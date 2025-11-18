import { Component, OnInit } from '@angular/core';
import { NavbarComponent } from '../../../components/navbar/navbar.component';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SearchBarComponent } from '../../../components/search-bar/search-bar.component';
import { MatIconModule } from '@angular/material/icon';
import { FlexCenterDirective } from '../../../directives/flex-center/flex-center.directive';
import { WorkspaceService } from '../../../services/people/workspace.service';
import { WorkSpace, Member } from '../../../models/people/workspace.interface';
import { FormatDatePipe } from '../../../pipes/format-date/format-date.pipe';
import { UserService } from '../../../services/user.service';
import { AddWorkspaceComponent } from '../../../components/people/add-workspace/add-workspace.component';

@Component({
  selector: 'app-workspace',
  imports: [NavbarComponent, CommonModule, FormsModule, SearchBarComponent, MatIconModule, FlexCenterDirective, FormatDatePipe, AddWorkspaceComponent],
  templateUrl: './workspace.component.html',
  styleUrl: './workspace.component.scss'
})
export class WorkspaceComponent implements OnInit {
  usId: string | null = sessionStorage.getItem('us_id');
  isAdd: boolean = false;

  ownerWorkspaces: WorkSpace[] = [];
  memberWorkspaces: WorkSpace[] = [];
  workspaces: WorkSpace[] = [];

  images: { us_id: string, img: string }[] = [];
  members: Member[] = [];
  memberImageMap: { [us_id: string]: string } = {};

  constructor(private workspaceService: WorkspaceService, private userService: UserService) {}

  ngOnInit() {
      this.loadWorkspace(); 
  }

  async loadWorkspace() {
    if (!this.usId) {
      console.warn("User ID rỗng!");
      return;
    }

    try {
      const response = await this.workspaceService.getWorkspaceOwner(this.usId);
      this.ownerWorkspaces = response.data;
      console.log(this.ownerWorkspaces);
    } catch (error) {
      console.error("Lỗi khi lấy sách Workspaces:", error);
    }

    try {
      const response = await this.workspaceService.getWorkspaceMember(this.usId);
      this.memberWorkspaces = response.data;
      console.log(this.memberWorkspaces);
    } catch (error) {
      console.error("Lỗi khi lấy sách Workspaces:", error);
    }

    this.workspaces = [...this.ownerWorkspaces, ...this.memberWorkspaces];
    this.members = this.workspaces
    .flatMap((m) => m.members ?? [])
    .filter((m): m is Member => m !== undefined && m !== null);

    await this.loadMemberImages();
  }

  async loadMemberImages() {
    try {
      const imagesData = await Promise.all(
        this.members.map(async (m) => {
          try {
            const response = await this.userService.userInfo(m.us_id);            
            return {
              us_id: m.us_id,
              img: response.us_img || '/assets/default-avatar.png'
            };
          } catch (error) {
            console.error(`Lỗi khi lấy ảnh của ${m.us_id}:`, error);
            return {
              us_id: m.us_id,
              img: '/assets/default-avatar.png'
            };
          }
        })
      );
      this.images = imagesData;
      this.memberImageMap = {};
      this.images.forEach(img => {
        this.memberImageMap[img.us_id] = img.img;
      });
      console.log("Danh sách ảnh members:", this.images);
    } catch (error) {
      console.error("Lỗi khi load danh sách ảnh members:", error);
    }
  }

  getMemberImagesByWorkspace(workspace: WorkSpace): string[] {
    if (!workspace.members) return [];
    return workspace.members
      .slice(0, 3)
      .map(m => this.memberImageMap[m.us_id] || '/assets/default-avatar.png')
      .filter(img => img !== undefined);
  }

  openAdd() {
    this.isAdd = true;
  }

  closeAdd() {
    this.isAdd = false;
  }
  
}
