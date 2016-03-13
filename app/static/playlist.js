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
var icon = null;

var PlayList = React.createClass({
  getInitialState: function () {
    return {play: false, playingIndex: null };
  },
  handleClick: function(index) {
    if (index === this.state.playingIndex){
      if (this.state.play){
        audioObject.pause();
        this.setState({
          play: false
        });
      }
      else{
        audioObject.play();
        this.setState({
          play: true
        });

      }
    }
    else {
      this.setState({play: true, playingIndex: index}});
      if (audioObject){
        audioObject.pause();
        audioObject.load();
      }
      audioObject = new Audio(data[index].preview_url);
      audioObject.play();

    }
  },
  render: function(){
    return (
      <div>
        <ul className="collection col s12">
        {
          data.map(function(m, index){
            if ((this.state.playingIndex===index) && this.state.play){
              icon = "pause";
            }
            else {
              icon="play_arrow";
            }
            return <Item  title={m.title} artist={m.artist} description={m.description} preview={m.preview_url} playingIndex={this.state.playingIndex} icon={icon} clickHandler={this.handleClick} index = {index}/>
          }, this)
        }
        </ul>
      </div>
    )
  }
})

var Item = React.createClass({
  handleClick: function() {
    this.props.clickHandler(this.props.index);  
  },
  render: function(){
    return (
      <div className="collection-item avatar hoverable">
        <i onBlur={this.handleClick} onClick={this.handleClick} className="material-icons circle red">{this.props.icon}</i>
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
