import { Component, OnInit, Input } from '@angular/core';
import {Post} from "../../models/Post";
import { HomeFeedService } from "../../services/home-feed.service";
import { SessionService } from "../../services/session.service";
import { PostCreationService} from "../../services/post-creation.service";
import { NewPostForm} from "../../models/NewPostForm";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  posts: Post[] = []
  numInitialPosts = 25;
  postsPerLoad = 10;
  currentPost = 0;
  token = "";

  //TODO Pass a session service with the token
  constructor(private homeFeed: HomeFeedService, private route : ActivatedRoute) {

    this.route.queryParams
      .subscribe(params => {
          this.token = params['token']
        }
      );
    console.log('token', this.token)
  }

  ngOnInit(): void {
    this.demanarPost();
  }

  demanarPost(){
    let requestParams = {
      "limit": this.postsPerLoad,
      "offset": this.currentPost,
    }
    // @ts-ignore
    this.homeFeed.getPostsFrom(requestParams, this.token).subscribe((newPosts: Object) => {
      // @ts-ignore
      let postList = newPosts['posts']
      for (let postNum = 0; postNum < postList.length; postNum++){
        this.posts.push(postList[postNum]);
        this.currentPost = this.currentPost +1;
      }
    }, (error: any) => {
      console.log(error);
    })

  }



  mockPosts(){
    const newPost: Post = {
      id: 12,
      text: "This is mock content for testing purposes testing testing 1231 23fdsfdsfdsfdsfdsfdsfdsfdsfdsfdfdsfdsfdsfdsfsdsfd vsdsfdsfds",
      time: "2022-10-02",
      archived: false,
      account_id: 12,
      account_name: "kermit",
      parent_id: 12
    };
    this.posts.push(newPost)
    this.posts.push(newPost)
    this.posts.push(newPost)
  }

}
