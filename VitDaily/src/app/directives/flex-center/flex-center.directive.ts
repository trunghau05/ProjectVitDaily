import { Directive, ElementRef, Renderer2, OnInit } from '@angular/core';

@Directive({
  selector: '[flexCenter]'
})
export class FlexCenterDirective implements OnInit {

  constructor(private el: ElementRef, private renderer: Renderer2) {}

  ngOnInit(): void {
    this.renderer.setStyle(this.el.nativeElement, 'display', 'flex');
    this.renderer.setStyle(this.el.nativeElement, 'justify-content', 'center');
    this.renderer.setStyle(this.el.nativeElement, 'align-items', 'center');
  }
}
