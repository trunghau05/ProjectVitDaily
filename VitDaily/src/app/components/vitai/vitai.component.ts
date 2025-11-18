import { Component, ElementRef, ViewChild, AfterViewChecked } from '@angular/core';
import { FlexCenterDirective } from '../../directives/flex-center/flex-center.directive';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from "@angular/forms";
import { VitaiService } from '../../services/vitai.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-vitai',
  imports: [FlexCenterDirective, CommonModule, MatIconModule, FormsModule],
  templateUrl: './vitai.component.html',
  styleUrl: './vitai.component.scss'
})
export class VitaiComponent {
  @ViewChild('chatContent') private chatContent!: ElementRef;
  isOpen = false;
  usInput = '';
  objectKeys = Object.keys;

  messages: { from: 'user' | 'bot', text?: string, json?: any }[] = [];

  constructor(private vitaiService: VitaiService, private router: Router) {}

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  private scrollToBottom() {
    try {
      this.chatContent.nativeElement.scrollTop = this.chatContent.nativeElement.scrollHeight;
    } catch (err) {}
  }

  toggleChat() {
    this.isOpen = !this.isOpen;
  }

  navigateTo(route: string) {
    this.router.navigate([`/person/detail-note/${route}`]);
  }

  handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault(); 
      this.sendMessage();
    }
  }

  async sendMessage() {
    if (!this.usInput.trim()) return; 
    this.messages.push({ from: 'user', text: this.usInput });
    
    try {
      const response = await this.vitaiService.chatVitai(this.usInput);
      let result = response.result || 'Xin lỗi, tôi chưa hiểu.';

      const jsonMatch = result.match(/```json([\s\S]*?)```/);

      if (jsonMatch) {
        const beforeText = result.split(jsonMatch[0])[0].trim(); 
        const afterText = result.split(jsonMatch[0])[1]?.trim(); 

        if (beforeText) {
          this.messages.push({ from: 'bot', text: beforeText });
        }

        try {
          const parsed = JSON.parse(jsonMatch[1].trim());
          this.messages.push({ from: 'bot', json: parsed });
        } catch (e) {
          this.messages.push({ from: 'bot', text: jsonMatch[1] });
        }

        if (afterText) {
          this.messages.push({ from: 'bot', text: afterText });
        }

      } else {
        this.messages.push({ from: 'bot', text: result });
      }

    } catch (error) {
      this.messages.push({ from: 'bot', text: 'Có lỗi xảy ra khi kết nối server.' });
    }

    this.usInput = ''; 
  }

  clearChat() {
    this.messages = [];
  }
}
