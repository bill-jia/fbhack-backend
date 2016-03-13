var all = [
  {
    title: "title",
    artist: 'artist',
    description: 'description',
    preview_url: 'http://d318706lgtcm8e.cloudfront.net/mp3-preview/f454c8224828e21fa146af84916fd22cb89cedc6'
  },
  {
    title: "title",
    artist: 'artist',
    description: 'description',
    preview_url: 'http://d318706lgtcm8e.cloudfront.net/mp3-preview/f454c8224828e21fa146af84916fd22cb89cedc6'
  },
  {
    title: "title",
    artist: 'artist',
    description: 'description',
    preview_url: 'http://d318706lgtcm8e.cloudfront.net/mp3-preview/f454c8224828e21fa146af84916fd22cb89cedc6'
  }
];

var audioObject = null;

var PlayList = React.createClass({

  render: function(){
    return (
      <div>
        <ul className="collection col s12">
        {
          all.map(function(m, index){
            return <Item  title={m.title} artist={m.artist} description={m.description} preview={m.preview_url}/>
          })
        }
        </ul>
      </div>
    )
  }
})

var Item = React.createClass({

  getInitialState: function(){
    return {
      play: false,
      icon: 'play_arrow'
    };
  },

  handlePlay: function(){
    if(this.state.play){
      audioObject.pause();
      this.setState({
        play: false,
        icon: 'play_arrow'
      });
    }
    else {
      audioObject = new Audio(this.props.preview);
      audioObject.play();
      this.setState({
        play: true,
        icon: 'pause'
      });
    }
  },

  render: function(){
    return (
      <div className="collection-item avatar hoverable">
        <i onBlur={this.handlePlay} onClick={this.handlePlay} className="material-icons circle red">{this.state.icon}</i>
        <span className="title">{this.props.title}</span>
        <p>{this.props.artist} <br/> {this.props.description}</p>
      </div>
    )
  }
})

ReactDOM.render(
  <PlayList/>,
  document.getElementById('playlist')
);
