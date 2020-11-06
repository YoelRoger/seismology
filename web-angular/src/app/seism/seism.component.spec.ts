import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SeismComponent } from './seism.component';

describe('SeismComponent', () => {
  let component: SeismComponent;
  let fixture: ComponentFixture<SeismComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SeismComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SeismComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
