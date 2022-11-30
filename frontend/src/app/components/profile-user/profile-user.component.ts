import { Component, OnInit } from '@angular/core';
import {Post} from "../../models/Post";
import {PostCreationService} from "../../services/post-creation.service";
import {ActivatedRoute} from "@angular/router";
import {GetNumPosts} from "../../models/GetNumPosts";

@Component({
  selector: 'app-profile-user',
  templateUrl: './profile-user.component.html',
  styleUrls: ['./profile-user.component.css']
})
export class ProfileUserComponent implements OnInit {
  postsUser: Post[] = []
  user!: string
  token!: string
  idUser!: string
  nameButton!: string
  numSeguidores!: number

  constructor(private postCreationService: PostCreationService, private route : ActivatedRoute) {
    this.route.queryParams
    .subscribe(params => {
        this.user = params["user"]
        this.token = params["token"]
        this.idUser = params["idUser"]
      }
      )
  }

  ngOnInit(): void {
    this.nameButton = "Follow"
    this.getPostsUser()
    this.isFollow()
    this.numFollowings()
  }

  isFollow() {
    this.postCreationService.isFollowUser(this.idUser, this.token).subscribe(
      (result) => {
        if(result.message != `Account [${this.idUser}] doesn't follow any account`) {
          this.nameButton = "UnFollow"
        }
      }
    )
  }

  numFollowings() {
    this.postCreationService.followList(this.idUser, this.token).subscribe(
      (result) => {
          this.numSeguidores = result.ListFollows.length
      }
    )
  }

  unFollowOrFollow() {
      if(this.nameButton == "Follow"){
          this.postCreationService.follow(this.idUser, this.token).subscribe(
          (result) => {
              this.nameButton = "unFollow"
              this.numFollowings()
          }
          )
      } else {
        this.postCreationService.unfollow(this.idUser, this.token).subscribe(
          (result) => {
              this.nameButton = "Follow"
              this.numFollowings()
          }
          )
      }
  }

  getPostsUser () {
    const posts: GetNumPosts = {
      limit: 10,
      offset: 0
    }
    this.postCreationService.getPostsSpecificUser(posts, this.token, this.idUser).subscribe(
      (result) => {
        console.log(result.posts)
        for (const post of result.posts) {
          this.postsUser.push(post)
          console.log(post.id)
        }
      }
    )
  }
}